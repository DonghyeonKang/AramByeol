package com.arambyeol.dto;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import jakarta.validation.constraints.Email;
import io.swagger.v3.oas.annotations.media.Schema;

@Data
@Schema(description = "회원가입 요청 DTO")
public class UserRequestDto {
    @NotBlank(message = "이메일은 필수입니다")
    @Email(message = "올바른 이메일 형식이 아닙니다")
    @Schema(description = "사용자 이메일", example = "user@example.com")
    private String username;

    @NotBlank(message = "비밀번호는 필수입니다")
    @Size(min = 8, message = "비밀번호는 최소 8자 이상이어야 합니다")
    @Schema(description = "사용자 비밀번호", example = "password123")
    private String password;
}