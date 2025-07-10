package com.arambyeol.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Email;
import lombok.Getter;
import io.swagger.v3.oas.annotations.media.Schema;

@Getter
@Schema(description = "로그인 요청 DTO")
public class LoginRequestDto {
    @NotBlank(message = "이메일은 필수입니다")
    @Email(message = "올바른 이메일 형식이 아닙니다")
    @Schema(description = "사용자 이메일", example = "user@example.com")
    private String username;

    @NotBlank(message = "비밀번호는 필수입니다")
    @Schema(description = "사용자 비밀번호", example = "password123")
    private String password;
} 