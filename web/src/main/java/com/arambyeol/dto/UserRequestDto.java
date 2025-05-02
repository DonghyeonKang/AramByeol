package com.arambyeol.dto;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

@Data
public class UserRequestDto {
    @NotBlank(message = "사용자 이름은 필수입니다")
    @Size(min = 4, max = 20, message = "사용자 이름은 4-20자 사이여야 합니다")
    private String username;

    @NotBlank(message = "비밀번호는 필수입니다")
    @Size(min = 8, message = "비밀번호는 최소 8자 이상이어야 합니다")
    private String password;
}