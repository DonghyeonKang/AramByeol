package com.arambyeol.dto;

import lombok.Builder;
import lombok.Getter;
import java.time.LocalDateTime;

@Getter
@Builder
public class ReviewResponseDto {
    private Long reviewId;
    private Long menuId;
    private String menuName;
    private String imgPath;
    private Integer score;
} 