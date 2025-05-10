package com.arambyeol.dto;

import com.arambyeol.domain.MealType;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class DailyMenuDto {
    private Integer menuId;
    private String menuName;
    private MealType mealType;
    private String course;
    private String imgPath;
    private double averageScore;
    private long reviewCount;
} 