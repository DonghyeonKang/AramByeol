package com.arambyeol.dto;

import lombok.Builder;
import lombok.Getter;
import io.swagger.v3.oas.annotations.media.Schema;
import com.arambyeol.domain.MealType;

@Getter
@Builder
@Schema(description = "일일 메뉴 DTO")
public class DailyMenuDto {
    @Schema(description = "메뉴 ID", example = "1")
    private Integer menuId;
    
    @Schema(description = "메뉴명", example = "김치찌개")
    private String menuName;
    
    @Schema(description = "식사 타입", example = "LUNCH")
    private MealType mealType;
    
    @Schema(description = "코스", example = "메인")
    private String course;
    
    @Schema(description = "이미지 경로", example = "/images/kimchi-jjigae.jpg")
    private String imgPath;
    
    @Schema(description = "평균 평점", example = "4.5")
    private double averageScore;
    
    @Schema(description = "리뷰 개수", example = "10")
    private int reviewCount;
} 