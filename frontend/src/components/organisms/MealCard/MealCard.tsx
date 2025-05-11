import { useState } from 'react';
import { Card } from '../../molecules/Card/Card';
import { ProcessedMeal } from '@/types/menu';
import { ReviewModal } from '../../molecules/ReviewModal/ReviewModal';
import './MealCard.css';

interface MealCardProps {
  meal: ProcessedMeal;
}

export const MealCard = ({ meal }: MealCardProps) => {
  const [selectedMenu, setSelectedMenu] = useState<string | null>(null);

  return (
    <>
      <Card className="meal-card">
        <div className="meal-header">
          <h3>{meal.type}</h3>
          <span className="meal-time">{meal.time}</span>
        </div>
        <div className="courses">
          {Object.entries(meal.courses).map(([course, menus]) => (
            <div key={course} className="course">
              <h4 className="course-title">{course}</h4>
              <ul className="menu-list">
                {menus.map((menu, index) => (
                  <li 
                    key={index} 
                    onClick={() => setSelectedMenu(menu)}
                    className="menu-item"
                  >
                    <span className="menu-name">{menu}</span>
                    <div className="menu-score">
                      <span className="material-icons">star</span>
                      <span>4.5</span>
                      <span className="review-count">(23)</span>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </Card>
      <ReviewModal
        isOpen={!!selectedMenu}
        onClose={() => setSelectedMenu(null)}
        menuName={selectedMenu || ''}
        score={4.5}
        reviewCount={23}
      />
    </>
  );
}; 