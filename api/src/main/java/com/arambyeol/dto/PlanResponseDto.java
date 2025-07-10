package com.arambyeol.dto;

import lombok.Builder;
import lombok.Getter;
import io.swagger.v3.oas.annotations.media.Schema;
import java.util.Map;
import com.arambyeol.domain.MealType;

@Getter
@Builder
@Schema(description = "식단 응답 DTO")
public class PlanResponseDto {
    @Schema(description = "날짜", example = "2024-03-20")
    private String date;
    
    @Schema(description = "식사 타입별 메뉴 목록")
    private Map<MealType, java.util.List<DailyMenuDto>> menusByMealType;
} 