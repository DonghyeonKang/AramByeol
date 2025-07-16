package com.arambyeol.controller;

import com.arambyeol.dto.LoginRequestDto;
import com.arambyeol.dto.TokenResponseDto;
import com.arambyeol.dto.UserRequestDto;
import com.arambyeol.dto.PasswordResetDto;
import com.arambyeol.dto.EmailRequestDto;
import com.arambyeol.dto.EmailVerifyDto;
import com.arambyeol.service.AuthService;
import com.arambyeol.service.EmailAuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletResponse;
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
    private final EmailAuthService emailAuthService;

    @Operation(summary = "회원 가입", description = "새로운 사용자를 등록합니다.")
    @PostMapping("/register")
    public ResponseEntity<?> register(@Valid @RequestBody UserRequestDto requestDto) {
        return ResponseEntity.ok(authService.register(requestDto));
    }

    @Operation(summary = "로그인 (웹용)", description = "사용자 인증 후 JWT 토큰을 HTTP Only 쿠키로 발급합니다.")
    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequestDto request, HttpServletResponse response) {
        TokenResponseDto tokenResponse = authService.login(request.getUsername(), request.getPassword());
        
        // Access Token 쿠키 설정
        Cookie accessTokenCookie = new Cookie("access_token", tokenResponse.getAccessToken());
        accessTokenCookie.setHttpOnly(true);
        accessTokenCookie.setSecure(true); // HTTPS에서만 전송
        accessTokenCookie.setPath("/");
        accessTokenCookie.setMaxAge(3600); // 1시간
        response.addCookie(accessTokenCookie);
        
        // Refresh Token 쿠키 설정
        Cookie refreshTokenCookie = new Cookie("refresh_token", tokenResponse.getRefreshToken());
        refreshTokenCookie.setHttpOnly(true);
        refreshTokenCookie.setSecure(true); // HTTPS에서만 전송
        refreshTokenCookie.setPath("/");
        refreshTokenCookie.setMaxAge(604800); // 7일
        response.addCookie(refreshTokenCookie);
        
        return ResponseEntity.ok().body("로그인 성공");
    }

    @Operation(summary = "로그인 (앱용)", description = "사용자 인증 후 JWT 토큰을 응답 본문으로 발급합니다.")
    @PostMapping("/login/app")
    public ResponseEntity<TokenResponseDto> loginForApp(@Valid @RequestBody LoginRequestDto request) {
        TokenResponseDto tokenResponse = authService.login(request.getUsername(), request.getPassword());
        return ResponseEntity.ok(tokenResponse);
    }

    @Operation(summary = "토큰 갱신", description = "Refresh Token을 사용하여 새로운 Access Token을 발급합니다.")
    @PostMapping("/refresh")
    public ResponseEntity<?> refreshToken(@CookieValue("refresh_token") String refreshToken, HttpServletResponse response) {
        TokenResponseDto tokenResponse = authService.refreshAccessToken(refreshToken);
        
        // 새로운 Access Token 쿠키 설정
        Cookie accessTokenCookie = new Cookie("access_token", tokenResponse.getAccessToken());
        accessTokenCookie.setHttpOnly(true);
        accessTokenCookie.setSecure(true);
        accessTokenCookie.setPath("/");
        accessTokenCookie.setMaxAge(3600); // 1시간
        response.addCookie(accessTokenCookie);
        
        return ResponseEntity.ok().body("토큰 갱신 성공");
    }

    @Operation(summary = "로그아웃", description = "사용자 로그아웃 및 쿠키 삭제")
    @PostMapping("/logout")
    public ResponseEntity<?> logout(@CookieValue("refresh_token") String refreshToken, HttpServletResponse response) {
        authService.logout(refreshToken);
        
        // 쿠키 삭제
        Cookie accessTokenCookie = new Cookie("access_token", null);
        accessTokenCookie.setHttpOnly(true);
        accessTokenCookie.setSecure(true);
        accessTokenCookie.setPath("/");
        accessTokenCookie.setMaxAge(0);
        response.addCookie(accessTokenCookie);
        
        Cookie refreshTokenCookie = new Cookie("refresh_token", null);
        refreshTokenCookie.setHttpOnly(true);
        refreshTokenCookie.setSecure(true);
        refreshTokenCookie.setPath("/");
        refreshTokenCookie.setMaxAge(0);
        response.addCookie(refreshTokenCookie);
        
        return ResponseEntity.ok().body("로그아웃 성공");
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
        return ResponseEntity.ok().body("비밀번호가 성공적으로 재설정되었습니다.");
    }

    @PostMapping("/send-verification")
    public ResponseEntity<?> sendVerification(@RequestBody EmailRequestDto request) {
        emailAuthService.sendVerificationCode(request.getEmail());
        return ResponseEntity.ok().build();
    }

    @PostMapping("/verify-code")
    public ResponseEntity<?> verifyCode(@RequestBody EmailVerifyDto request) {
        boolean result = emailAuthService.verifyCode(request.getEmail(), request.getCode());
        return ResponseEntity.ok(result);
    }
} 