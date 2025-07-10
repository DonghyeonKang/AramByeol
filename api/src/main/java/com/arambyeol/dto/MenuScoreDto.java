package com.arambyeol.dto;

import lombok.Builder;
import lombok.Getter;
import io.swagger.v3.oas.annotations.media.Schema;

@Getter
@Builder
@Schema(description = "메뉴 평점 DTO")
public class MenuScoreDto {
    @Schema(description = "메뉴 ID", example = "1")
    private Integer menuId;
    
    @Schema(description = "메뉴명", example = "김치찌개")
    private String menuName;
    
    @Schema(description = "평균 평점", example = "4.5")
    private double averageScore;
    
    @Schema(description = "리뷰 개수", example = "10")
    private long reviewCount;
} 