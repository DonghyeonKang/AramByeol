import { useState, useEffect } from 'react';
// import { MealCard } from '../../components/organisms/MealCard/MealCard';  // 사용하지 않는 import 제거
import { ProcessedMeal } from '@/types/menu';
import { api } from '@/services/api';
import './Home.css';
import { MealList } from '@/components/organisms/MealList/MealList';

interface MenuItem {
  menuId: number;
  menuName: string;
  mealType: 'BREAKFAST' | 'LUNCH' | 'DINNER';
  course: string;
  imgPath: string;
  averageScore: number;
  reviewCount: number;
}

interface ApiResponse {
  date: string;
  menusByMealType: {
    BREAKFAST: MenuItem[];
    LUNCH: MenuItem[];
    DINNER: MenuItem[];
  };
}

export const Home = () => {
  // 오늘 날짜 계산 (UTC 기준)
  const today = new Date();
  today.setHours(0, 0, 0, 0);  // 시간을 00:00:00으로 설정
  const todayString = new Date(today.getTime() - (today.getTimezoneOffset() * 60000))
    .toISOString()
    .split('T')[0];

  const [meals, setMeals] = useState<ProcessedMeal[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchTodayMenu = async () => {
      setIsLoading(true);
      try {
        const dailyPlan = await api.getDailyPlan(todayString);
        const processedMeals = convertApiResponseToProcessedMeals(dailyPlan);
        setMeals(processedMeals);
      } catch (error) {
        console.error('Failed to fetch today menu:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTodayMenu();
  }, []);

  // API 응답을 ProcessedMeal 형식으로 변환하는 함수
  const convertApiResponseToProcessedMeals = (apiResponse: ApiResponse): ProcessedMeal[] => {
    return Object.entries(apiResponse.menusByMealType).map(([mealType, menus]) => {
      // 코스별로 메뉴 그룹화
      const courseMenus = menus.reduce((acc: { [key: string]: string[] }, menu) => {
        const courseName = menu.course.split('/')[1];  // "A코스/한식" -> "한식"
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
    });
  };

  const formatDate = () => {
    const date = new Date();
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const weekDay = ['일', '월', '화', '수', '목', '금', '토'][date.getDay()];
    
    return `${year}년 ${month}월 ${day}일 ${weekDay}요일`;
  };

  return (
    <div className="home">
      <section className="hero-section">
        <h1>오늘의 식단</h1>
        <p>{formatDate()} 경상국립대학교 아람관 메뉴</p>
      </section>
      
      <main className="main-content">
        <section className="meals-section">
          {isLoading ? (
            <div className="loading">로딩 중...</div>
          ) : (
            <MealList meals={meals} layout="row" />
          )}
        </section>
      </main>
    </div>
  );
}; 