import { useState } from 'react';
import { MealCard } from '../../components/organisms/MealCard/MealCard';
import { ProcessedMeal } from '@/types/menu';
import './Weekly.css';
import { MealList } from '@/components/organisms/MealList/MealList';

interface DateButton {
  day: string;
  date: string;
  fullDate: string;
}

export const Weekly = () => {
  const [weekOffset, setWeekOffset] = useState(0); // 0: 이번주, 1: 다음주

  // 주차별 날짜 버튼 생성
  const getWeekDates = (offset: number): DateButton[] => {
    const days = ['일', '월', '화', '수', '목', '금', '토'];
    const today = new Date();
    const monday = new Date(today);
    monday.setDate(today.getDate() - today.getDay() + 1 + (offset * 7));
    
    return Array.from({ length: 7 }, (_, i) => {
      const date = new Date(monday);
      date.setDate(monday.getDate() + i);
      return {
        day: days[date.getDay()],
        date: `${date.getMonth() + 1}/${date.getDate()}`,
        fullDate: date.toISOString().split('T')[0],
      };
    });
  };

  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [weekDates, setWeekDates] = useState(getWeekDates(0));

  // 주차 변경 처리
  const handleWeekChange = (newOffset: number) => {
    setWeekOffset(newOffset);
    const newDates = getWeekDates(newOffset);
    setWeekDates(newDates);
    setSelectedDate(newDates[1].fullDate); // 월요일 선택
  };

  // 요일별 목업 데이터
  const mockMealsByDay: { [key: string]: ProcessedMeal[] } = {
    '월': [
      {
        type: '조식',
        time: '07:30 - 09:00',
        courses: {
          '한식': ['흰쌀밥', '된장국', '고등어구이', '김치'],
          '일품': ['토스트', '스크램블에그', '샐러드']
        }
      },
      {
        type: '중식',
        time: '11:30 - 13:30',
        courses: {
          '한식': ['흰쌀밥', '김치찌개', '제육볶음', '김치'],
          '일품': ['돈까스', '양배추샐러드'],
          '양식': ['치킨버거', '감자튀김']
        }
      },
      {
        type: '석식',
        time: '17:30 - 19:00',
        courses: {
          '한식': ['흰쌀밥', '순대국', '닭갈비', '김치'],
          '일품': ['돈까스덮밥', '유부된장국'],
          '양식': ['치킨까스', '샐러드']
        }
      }
    ],
    '화': [
      {
        type: '조식',
        time: '07:30 - 09:00',
        courses: {
          '한식': ['흰쌀밥', '미역국', '계란말이', '김치'],
          '일품': ['샌드위치', '요구르트', '과일']
        }
      },
      {
        type: '중식',
        time: '11:30 - 13:30',
        courses: {
          '한식': ['흰쌀밥', '순두부찌개', '불고기', '김치'],
          '일품': ['우동', '튀김'],
          '양식': ['파스타', '샐러드']
        }
      },
      {
        type: '석식',
        time: '17:30 - 19:00',
        courses: {
          '한식': ['흰쌀밥', '김치찌개', '고등어구이', '김치'],
          '일품': ['비빔밥', '계란후라이'],
          '양식': ['스파게티', '마늘빵']
        }
      }
    ],
    '수': [
      {
        type: '조식',
        time: '07:30 - 09:00',
        courses: {
          '한식': ['흰쌀밥', '콩나물국', '동그랑땡', '김치'],
          '일품': ['핫도그', '우유', '씨리얼']
        }
      },
      {
        type: '중식',
        time: '11:30 - 13:30',
        courses: {
          '한식': ['흰쌀밥', '육개장', '코다리조림', '김치'],
          '일품': ['카레라이스', '계란후라이'],
          '양식': ['피자', '콜라']
        }
      },
      {
        type: '석식',
        time: '17:30 - 19:00',
        courses: {
          '한식': ['흰쌀밥', '된장찌개', '제육볶음', '김치'],
          '일품': ['김치볶음밥', '계란국'],
          '양식': ['치즈돈까스', '샐러드']
        }
      }
    ],
    '목': [
      {
        type: '조식',
        time: '07:30 - 09:00',
        courses: {
          '한식': ['흰쌀밥', '북어국', '두부조림', '김치'],
          '일품': ['프렌치토스트', '딸기잼', '우유']
        }
      },
      {
        type: '중식',
        time: '11:30 - 13:30',
        courses: {
          '한식': ['흰쌀밥', '청국장', '닭갈비', '김치'],
          '일품': ['짜장면', '단무지'],
          '양식': ['함박스테이크', '샐러드']
        }
      },
      {
        type: '석식',
        time: '17:30 - 19:00',
        courses: {
          '한식': ['흰쌀밥', '육개장', '코다리조림', '김치'],
          '일품': ['야채볶음밥', '미소국'],
          '양식': ['포크커틀릿', '감자튀김']
        }
      }
    ],
    '금': [
      {
        type: '조식',
        time: '07:30 - 09:00',
        courses: {
          '한식': ['흰쌀밥', '어묵국', '김치볶음', '김치'],
          '일품': ['베이글', '크림치즈', '과일']
        }
      },
      {
        type: '중식',
        time: '11:30 - 13:30',
        courses: {
          '한식': ['흰쌀밥', '감자탕', '갈치구이', '김치'],
          '일품': ['냉면', '만두'],
          '양식': ['오므라이스', '샐러드']
        }
      },
      {
        type: '석식',
        time: '17:30 - 19:00',
        courses: {
          '한식': ['흰쌀밥', '청국장', '불고기', '김치'],
          '일품': ['잔치국수', '김밥'],
          '양식': ['치킨버거', '콜라']
        }
      }
    ],
    '토': [
      {
        type: '조식',
        time: '08:00 - 09:30',
        courses: {
          '한식': ['흰쌀밥', '순두부찌개', '메추리알장조림', '김치'],
          '일품': ['크로와상', '딸기잼', '우유']
        }
      },
      {
        type: '중식',
        time: '11:30 - 13:30',
        courses: {
          '한식': ['흰쌀밥', '부대찌개', '오징어볶음', '김치'],
          '일품': ['라면', '김밥'],
          '양식': ['핫도그', '감자튀김']
        }
      },
      {
        type: '석식',
        time: '17:30 - 19:00',
        courses: {
          '한식': ['흰쌀밥', '삼겹살김치찌개', '계란말이', '김치'],
          '일품': ['우동', '튀김'],
          '양식': ['피자', '콜라']
        }
      }
    ],
    '일': [
      {
        type: '조식',
        time: '08:00 - 09:30',
        courses: {
          '한식': ['흰쌀밥', '된장국', '계란후라이', '김치'],
          '일품': ['토스트', '딸기잼', '우유']
        }
      },
      {
        type: '중식',
        time: '11:30 - 13:30',
        courses: {
          '한식': ['흰쌀밥', '김치찌개', '제육볶음', '김치'],
          '일품': ['우동', '튀김'],
          '양식': ['햄버거', '콜라']
        }
      },
      {
        type: '석식',
        time: '17:30 - 19:00',
        courses: {
          '한식': ['흰쌀밥', '부대찌개', '동그랑땡', '김치'],
          '일품': ['볶음우동', '군만두'],
          '양식': ['치즈버거', '감자튀김']
        }
      }
    ]
  };

  // 선택된 날짜의 요일에 해당하는 메뉴 가져오기
  const getSelectedDayMeals = () => {
    const selectedDay = weekDates.find(date => date.fullDate === selectedDate)?.day;
    return mockMealsByDay[selectedDay || '월'] || [];
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
            onClick={() => handleWeekChange(0)}
            disabled={weekOffset === 0}
          >
            <span className="material-icons">chevron_left</span>
          </button>

          {weekDates.map((dateBtn) => (
            <button
              key={dateBtn.fullDate}
              className={`date-button ${selectedDate === dateBtn.fullDate ? 'active' : ''}`}
              onClick={() => setSelectedDate(dateBtn.fullDate)}
            >
              <span className="day">{dateBtn.day}</span>
              <span className="date">{dateBtn.date}</span>
            </button>
          ))}

          <button 
            className="arrow-button"
            onClick={() => handleWeekChange(1)}
            disabled={weekOffset === 1}
          >
            <span className="material-icons">chevron_right</span>
          </button>
        </nav>

        <MealList meals={getSelectedDayMeals()} layout="grid" />
      </main>
    </div>
  );
}; 