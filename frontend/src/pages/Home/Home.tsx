import { useState, useEffect } from 'react';
import { MealCard } from '../../components/organisms/MealCard/MealCard';
import { ProcessedMeal } from '@/types/menu';
import './Home.css';

// 목업 데이터
const mockMeals: ProcessedMeal[] = [
  {
    type: '조식',
    time: '07:30 - 09:00',
    courses: {
      '한식': ['흰쌀밥', '미역국', '계란말이', '김치', '깍두기'],
      '일품': ['토스트', '스크램블에그', '샐러드', '우유']
    }
  },
  {
    type: '중식',
    time: '11:30 - 13:30',
    courses: {
      '한식': ['흰쌀밥', '된장찌개', '제육볶음', '김치', '깍두기'],
      '일품': ['돈까스', '양배추샐러드', '우동'],
      '양식': ['치킨버거', '감자튀김', '콜라']
    }
  },
  {
    type: '석식',
    time: '17:30 - 19:00',
    courses: {
      '한식': ['흰쌀밥', '김치찌개', '고등어구이', '김치', '깍두기'],
      '일품': ['비빔밥', '계란후라이', '미소국']
    }
  }
];

export const Home = () => {
  const [meals, setMeals] = useState<ProcessedMeal[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // 목업 데이터 사용
    setTimeout(() => {
      setMeals(mockMeals);
      setIsLoading(false);
    }, 500); // 로딩 효과를 보기 위한 지연
  }, []);

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
      <main className="main-content">
        <section className="hero-section">
          <h1>오늘의 식단</h1>
          <p>{formatDate()} 경상국립대학교 아람관 메뉴</p>
        </section>
        <section className="meals-section">
          {isLoading ? (
            <div className="loading">로딩 중...</div>
          ) : (
            meals.map((meal, index) => (
              <MealCard key={index} meal={meal} />
            ))
          )}
        </section>
      </main>
    </div>
  );
}; 