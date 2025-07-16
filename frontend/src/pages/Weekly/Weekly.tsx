import { useState, useEffect } from 'react';
import { ProcessedMeal } from '@/types/menu';
import { api } from '@/services/api';
import './Weekly.css';
import { MealList } from '@/components/organisms/MealList/MealList';

interface DateButton {
  day: string;
  date: string;
  fullDate: string;
}

interface MenuItem {
  menuId: number;
  menuName: string;
  mealType: 'BREAKFAST' | 'LUNCH' | 'DINNER';
  course: string;
  imgPath: string;
  averageScore: number;
  reviewCount: number;
}

interface DailyMenu {
  date: string;
  menusByMealType: {
    BREAKFAST?: MenuItem[];
    LUNCH?: MenuItem[];
    DINNER?: MenuItem[];
  };
}

export const Weekly = () => {
  const today = new Date().toISOString().split('T')[0];  // 오늘 날짜
  const [weekOffset, setWeekOffset] = useState(0);
  const [selectedDate, setSelectedDate] = useState(today);  // 초기값을 오늘 날짜로
  const [weekDates, setWeekDates] = useState<DateButton[]>([]);
  const [meals, setMeals] = useState<ProcessedMeal[]>([]);
  const [weeklyData, setWeeklyData] = useState<DailyMenu[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initializeWeek = async () => {
      setIsLoading(true);
      const newDates = getWeekDates(0);  // 현재 주차
      setWeekDates(newDates);

      // 오늘 날짜가 weekDates에 있으면 그 날짜를 선택, 없으면 첫 번째 날짜
      const todayBtn = newDates.find(d => d.fullDate === today);
      const initialDate = todayBtn ? todayBtn.fullDate : newDates[0].fullDate;
  
      try {
        const weeklyPlan = await api.getWeeklyPlan(initialDate); // 오늘 또는 첫 번째 날짜 기준 요청
        setWeeklyData(weeklyPlan);
  
        // 오늘 또는 첫 번째 날짜를 기준으로 렌더링
        const processedMeals = convertApiResponseToProcessedMeals(weeklyPlan, initialDate);
        setMeals(processedMeals);
        setSelectedDate(initialDate); // 오늘 또는 첫 번째 날짜 선택
      } catch (error) {
        console.error('Failed to fetch weekly plan:', error);
      } finally {
        setIsLoading(false);
      }
    };

    initializeWeek();
  }, []);

  // 주차별 날짜 버튼 생성
  const getWeekDates = (offset: number): DateButton[] => {
    const days = ['월', '화', '수', '목', '금', '토', '일'];  // 월요일부터 시작
    const today = new Date();
    const monday = new Date(today);
    
    // 이번 주 월요일로 설정 (정확한 계산)
    monday.setHours(0, 0, 0, 0);  // 시간을 00:00:00으로 설정
    monday.setDate(today.getDate() - ((today.getDay() + 6) % 7));
    monday.setDate(monday.getDate() + (offset * 7));
    
    return Array.from({ length: 7 }, (_, i) => {
      const date = new Date(monday);
      date.setDate(monday.getDate() + i);
      // UTC 기준으로 날짜 문자열 생성
      const fullDate = new Date(date.getTime() - (date.getTimezoneOffset() * 60000))
        .toISOString()
        .split('T')[0];
      
      return {
        day: days[i],
        date: `${date.getMonth() + 1}/${date.getDate()}`,
        fullDate: fullDate,
      };
    });
  };

  // 주차 변경 처리
  const handleWeekChange = async (newOffset: number) => {
    setIsLoading(true);
    setWeekOffset(newOffset);
    const newDates = getWeekDates(newOffset);
    setWeekDates(newDates);
    
    try {
      const weeklyPlan = await api.getWeeklyPlan(today);  // 오늘 날짜로 요청
      setWeeklyData(weeklyPlan);
      handleDateSelect(newDates[0].fullDate);  // 첫 번째 날짜 선택
    } catch (error) {
      console.error('Failed to fetch weekly plan:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // 날짜 선택 처리
  const handleDateSelect = (date: string) => {
    setSelectedDate(date);  // CSS 활성화를 위한 날짜 선택
    const processedMeals = convertApiResponseToProcessedMeals(weeklyData, date);
    setMeals(processedMeals);
  };

  // API 응답을 ProcessedMeal 형식으로 변환하는 함수
  const convertApiResponseToProcessedMeals = (apiResponse: DailyMenu[], date: string): ProcessedMeal[] => {
    const selectedDayMenu = apiResponse.find(menu => menu.date === date);
    
    if (!selectedDayMenu || !selectedDayMenu.menusByMealType) {
      return [];
    }

    // 식사 타입 순서 정의
    const mealTypeOrder = ['BREAKFAST', 'LUNCH', 'DINNER'];
    
    return mealTypeOrder
      .map(mealType => {
        const menus = selectedDayMenu.menusByMealType[mealType as keyof typeof selectedDayMenu.menusByMealType];
        if (!menus) return null;

        // 코스별로 메뉴 그룹화
        const courseMenus = menus.reduce((acc: { [key: string]: string[] }, menu) => {
          const courseName = menu.course.split('/')[1];
          if (!acc[courseName]) {
            acc[courseName] = [];
          }
          acc[courseName].push(menu.menuName);
          return acc;
        }, {});

        return {
          type: mealType === 'BREAKFAST' ? '조식' : 
                mealType === 'LUNCH' ? '중식' : '석식',
          time: mealType === 'BREAKFAST' ? '07:30 - 09:00' :
                mealType === 'LUNCH' ? '11:30 - 13:30' : '17:30 - 19:00',
          courses: courseMenus
        };
      })
      .filter((meal): meal is ProcessedMeal => meal !== null);
  };

  return (
    <div className="weekly-page">
      <section className="hero-section">
        <h1>주간 식단</h1>
        <p>아람관 식단을 확인하세요</p>
      </section>
      
      <main className="main-content">
        <nav className="date-navigation">
          <button 
            className="arrow-button"
            onClick={() => handleWeekChange(weekOffset - 1)}
            disabled={weekOffset === 0}
          >
            <span className="material-icons">chevron_left</span>
          </button>

          {weekDates.map((dateBtn) => (
            <button
              key={dateBtn.fullDate}
              className={`date-button ${selectedDate === dateBtn.fullDate ? 'active' : ''}`}
              onClick={() => handleDateSelect(dateBtn.fullDate)}
            >
              <span className="day">{dateBtn.day}</span>
              <span className="date">{dateBtn.date}</span>
            </button>
          ))}

          <button 
            className="arrow-button"
            onClick={() => handleWeekChange(weekOffset + 1)}
            disabled={weekOffset === 1}
          >
            <span className="material-icons">chevron_right</span>
          </button>
        </nav>

        {isLoading ? (
          <div className="loading">로딩 중...</div>
        ) : meals.length > 0 ? (
          <MealList meals={meals} layout="grid" />
        ) : (
          <div className="no-menu">
            <p>해당 날짜의 메뉴가 없습니다.</p>
          </div>
        )}
      </main>
    </div>
  );
}; 