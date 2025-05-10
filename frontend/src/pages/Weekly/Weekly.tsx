import { useState, useEffect } from 'react';
import { Card } from '../../components/molecules/Card/Card';
import './Weekly.css';

interface Meal {
  type: '조식' | '중식' | '석식';
  menu: string[];
  time: string;
}

interface DayMeals {
  date: string;
  dayOfWeek: string;
  meals: Meal[];
}

export const Weekly = () => {
  const [weeklyMeals, setWeeklyMeals] = useState<DayMeals[]>([]);
  const [selectedDate, setSelectedDate] = useState<string>('');

  useEffect(() => {
    const fetchWeeklyMeals = async () => {
      try {
        const response = await fetch('/api/meals/weekly');
        const data = await response.json();
        setWeeklyMeals(data);
        if (data.length > 0) {
          setSelectedDate(data[0].date);
        }
      } catch (error) {
        console.error('Failed to fetch weekly meals:', error);
      }
    };

    fetchWeeklyMeals();
  }, []);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', { month: 'long', day: 'numeric' });
  };

  const formatDateForHero = () => {
    const date = new Date();
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const weekDay = ['일', '월', '화', '수', '목', '금', '토'][date.getDay()];
    
    return `${year}년 ${month}월 ${day}일 ${weekDay}요일`;
  };

  return (
    <div className="weekly-page">
      <main className="main-content">
        <section className="hero-section">
          <h1>주간 식단</h1>
          <p>경상국립대학교 아람관 주간 메뉴</p>
        </section>
        <section className="weekly-header">
          <div className="date-navigation">
            {weeklyMeals.map((day) => (
              <button
                key={day.date}
                className={`date-button ${selectedDate === day.date ? 'active' : ''}`}
                onClick={() => setSelectedDate(day.date)}
              >
                <span className="day">{day.dayOfWeek}</span>
                <span className="date">{formatDate(day.date)}</span>
              </button>
            ))}
          </div>
        </section>
        <section className="meals-grid">
          {weeklyMeals
            .find((day) => day.date === selectedDate)
            ?.meals.map((meal, index) => (
              <Card key={index} className="meal-card">
                <div className="meal-header">
                  <h3>{meal.type}</h3>
                  <span className="meal-time">{meal.time}</span>
                </div>
                <ul className="menu-list">
                  {meal.menu.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </Card>
            ))}
        </section>
      </main>
    </div>
  );
}; 