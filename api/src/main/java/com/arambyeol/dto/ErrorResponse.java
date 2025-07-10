package com.arambyeol.dto;

import lombok.Builder;
import lombok.Getter;
import io.swagger.v3.oas.annotations.media.Schema;
import java.time.LocalDateTime;
import java.util.List;

@Getter
@Builder
@Schema(description = "에러 응답 DTO")
public class ErrorResponse {
    @Schema(description = "에러 발생 시간", example = "2024-03-20T10:30:00")
    private final LocalDateTime timestamp;
    
    @Schema(description = "HTTP 상태 코드", example = "400")
    private final int status;
    
    @Schema(description = "에러 타입", example = "Bad Request")
    private final String error;
    
    @Schema(description = "에러 메시지", example = "입력값 검증에 실패했습니다")
    private final String message;
    
    @Schema(description = "요청 경로", example = "/api/auth/login")
    private final String path;
    
    @Schema(description = "필드별 에러 목록")
    private final List<FieldError> fieldErrors;

    @Getter
    @Builder
    @Schema(description = "필드 에러 DTO")
    public static class FieldError {
        @Schema(description = "필드명", example = "username")
        private final String field;
        
        @Schema(description = "에러 메시지", example = "이메일 형식이 올바르지 않습니다")
        private final String message;
    }
} 