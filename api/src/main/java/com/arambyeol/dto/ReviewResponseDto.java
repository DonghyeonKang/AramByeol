package com.arambyeol.dto;

import lombok.Builder;
import lombok.Getter;
import io.swagger.v3.oas.annotations.media.Schema;

@Getter
@Builder
@Schema(description = "리뷰 응답 DTO")
public class ReviewResponseDto {
    @Schema(description = "리뷰 ID", example = "1")
    private Long reviewId;
    
    @Schema(description = "메뉴 ID", example = "1")
    private Integer menuId;
    
    @Schema(description = "사용자명", example = "user@example.com")
    private String username;
    
    @Schema(description = "메뉴명", example = "김치찌개")
    private String menuName;
    
    @Schema(description = "이미지 경로", example = "/images/kimchi-jjigae.jpg")
    private String imgPath;
    
    @Schema(description = "평점", example = "4")
    private Integer score;
} 