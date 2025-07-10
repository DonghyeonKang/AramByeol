package com.arambyeol.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;
import lombok.Getter;
import lombok.Setter;
import io.swagger.v3.oas.annotations.media.Schema;

@Getter
@Setter
@Schema(description = "리뷰 작성 요청 DTO")
public class ReviewRequestDto {
    @NotNull(message = "메뉴 ID는 필수입니다")
    @Schema(description = "메뉴 ID", example = "1")
    private Integer menuId;

    @NotNull(message = "평점은 필수입니다")
    @Min(value = 1, message = "평점은 1점 이상이어야 합니다")
    @Max(value = 5, message = "평점은 5점 이하여야 합니다")
    @Schema(description = "평점 (1-5점)", example = "4")
    private Integer score;
} 