package com.arambyeol.dto;

import lombok.Builder;
import lombok.Getter;
import java.util.List;
import java.util.Map;
import com.arambyeol.domain.MealType;

@Getter
@Builder
public class PlanResponseDto {
    private String date;
    private Map<MealType, List<DailyMenuDto>> menusByMealType;
} 