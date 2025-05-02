package com.arambyeol.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class MenuScoreDto {
    private Long menuId;
    private String menuName;
    private double averageScore;
    private long reviewCount;
} 