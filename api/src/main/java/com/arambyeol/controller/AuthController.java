package com.arambyeol.controller;

import com.arambyeol.dto.LoginRequestDto;
import com.arambyeol.dto.TokenResponseDto;
import com.arambyeol.dto.UserRequestDto;
import com.arambyeol.dto.PasswordResetDto;
import com.arambyeol.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Tag(name = "Auth", description = "인증 관련 API")
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {
    private final AuthService authService;

    @Operation(summary = "회원 가입", description = "새로운 사용자를 등록합니다.")
    @PostMapping("/register")
    public ResponseEntity<?> register(@Valid @RequestBody UserRequestDto requestDto) {
        return ResponseEntity.ok(authService.register(requestDto));
    }

    @Operation(summary = "로그인", description = "사용자 인증 후 JWT 토큰을 발급합니다.")
    @PostMapping("/login")
    public ResponseEntity<TokenResponseDto> login(@Valid @RequestBody LoginRequestDto request) {
        String token = authService.login(request.getUsername(), request.getPassword());
        return ResponseEntity.ok(new TokenResponseDto(token));
    }

    @Operation(summary = "사용자명 중복 확인", description = "사용자명의 중복 여부를 확인합니다.")
    @GetMapping("/check/{username}")
    public ResponseEntity<?> checkUsername(@PathVariable String username) {
        return ResponseEntity.ok(authService.checkUsernameDuplicate(username));
    }

    @Operation(summary = "비밀번호 재설정", description = "사용자의 비밀번호를 재설정합니다.")
    @PostMapping("/password/reset")
    public ResponseEntity<?> resetPassword(@Valid @RequestBody PasswordResetDto resetDto) {
        authService.resetPassword(resetDto);
        return ResponseEntity.ok().build();
    }
} 