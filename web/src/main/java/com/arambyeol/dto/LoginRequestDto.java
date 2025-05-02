package com.arambyeol.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Getter;

@Getter
public class LoginRequestDto {
    @NotBlank(message = "사용자명은 필수입니다")
    private String username;

    @NotBlank(message = "비밀번호는 필수입니다")
    private String password;
} 