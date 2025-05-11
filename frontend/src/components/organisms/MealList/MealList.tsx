import { ProcessedMeal } from '@/types/menu';
import { MealCard } from '../MealCard/MealCard';
import './MealList.css';

interface MealListProps {
  meals: ProcessedMeal[];
  layout?: 'row' | 'grid';  // row: 오늘의 식단용, grid: 주간 식단용
}

export const MealList = ({ meals, layout = 'row' }: MealListProps) => {
  return (
    <div className={`meal-list ${layout}`}>
      {meals.map((meal, index) => (
        <MealCard key={index} meal={meal} />
      ))}
    </div>
  );
}; 