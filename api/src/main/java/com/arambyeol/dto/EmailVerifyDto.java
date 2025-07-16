package com.arambyeol.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class EmailVerifyDto {
    private String email;
    private String code;
} 