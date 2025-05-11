export type MealType = 'BREAKFAST' | 'LUNCH' | 'DINNER';

export interface MenuItem {
  menuId: number;
  menuName: string;
  mealType: MealType;
  course: string;
  imgPath: string;
  averageScore: number;
  reviewCount: number;
}

export interface MenuResponse {
  date: string;
  menusByMealType: {
    [course: string]: MenuItem[];
  };
}

export interface ProcessedMeal {
  type: '조식' | '중식' | '석식';
  time: string;
  courses: {
    [course: string]: string[];  // course별 메뉴 목록
  };
} 