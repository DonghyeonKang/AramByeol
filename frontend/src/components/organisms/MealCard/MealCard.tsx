import { Card } from '../../molecules/Card/Card';
import './MealCard.css';

interface Meal {
  type: '조식' | '중식' | '석식';
  menu: string[];
  time: string;
}

interface MealCardProps {
  meal: Meal;
}

export const MealCard = ({ meal }: MealCardProps) => {
  return (
    <Card className="meal-card">
      <div className="meal-header">
        <h3>{meal.type}</h3>
        <span className="meal-time">{meal.time}</span>
      </div>
      <ul className="menu-list">
        {meal.menu.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </Card>
  );
}; 