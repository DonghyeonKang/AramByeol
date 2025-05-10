import { useState, useEffect } from 'react';
import { MealCard } from '../../components/organisms/MealCard/MealCard';
import './Home.css';

interface Meal {
  type: '조식' | '중식' | '석식';
  menu: string[];
  time: string;
}

// 목업 데이터
const mockMeals: Meal[] = [
  {
    type: '조식',
    time: '08:00 - 09:30',
    menu: [
      '흰쌀밥',
      '미역국',
      '계란말이',
      '김치',
      '깍두기'
    ]
  },
  {
    type: '중식',
    time: '11:00 - 14:00',
    menu: [
      '흰쌀밥',
      '된장찌개',
      '제육볶음',
      '김치',
      '깍두기',
      '단무지'
    ]
  },
  {
    type: '석식',
    time: '17:00 - 19:00',
    menu: [
      '흰쌀밥',
      '김치찌개',
      '고등어구이',
      '김치',
      '깍두기',
      '단무지'
    ]
  }
];

export const Home = () => {
  const [meals, setMeals] = useState<Meal[]>([
    {
      type: '조식',
      time: '08:00 - 09:30',
      menu: ['로딩중...']
    },
    {
      type: '중식',
      time: '11:00 - 14:00',
      menu: ['로딩중...']
    },
    {
      type: '석식',
      time: '17:00 - 19:00',
      menu: ['로딩중...']
    }
  ]);

  useEffect(() => {
    const fetchMeals = async () => {
      try {
        // 개발 환경에서는 목업 데이터 사용
        if (import.meta.env.DEV) {
          setMeals(mockMeals);
          return;
        }

        const response = await fetch('/api/meals/today');
        if (!response.ok) {
          throw new Error('서버 응답 오류');
        }
        const data = await response.json();
        setMeals(data);
      } catch (error) {
        console.error('식단 정보를 불러오는데 실패했습니다:', error);
        // 에러 발생 시 목업 데이터로 대체
        setMeals(mockMeals);
      }
    };

    fetchMeals();
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
          {meals.map((meal, index) => (
            <MealCard key={index} meal={meal} />
          ))}
        </section>
      </main>
    </div>
  );
}; 