package com.arambyeol.dto;

import lombok.Builder;
import lombok.Getter;
import io.swagger.v3.oas.annotations.media.Schema;
import java.util.List;

@Getter
@Builder
@Schema(description = "페이지 응답 DTO")
public class PageResponseDto<T> {
    @Schema(description = "데이터 목록")
    private List<T> content;
    
    @Schema(description = "현재 페이지 번호", example = "0")
    private int pageNumber;
    
    @Schema(description = "페이지 크기", example = "10")
    private int pageSize;
    
    @Schema(description = "전체 요소 개수", example = "100")
    private long totalElements;
    
    @Schema(description = "전체 페이지 개수", example = "10")
    private int totalPages;
    
    @Schema(description = "다음 페이지 존재 여부", example = "true")
    private boolean hasNext;
    
    @Schema(description = "이전 페이지 존재 여부", example = "false")
    private boolean hasPrevious;
} 