package com.arambyeol.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    private final JwtTokenProvider jwtTokenProvider;
    
    // 인증이 필요 없는 경로들
    private static final List<String> EXCLUDED_PATHS = Arrays.asList(
        "/auth/login",
        "/auth/register", 
        "/auth/check",
        "/auth/password/reset",
        "/plans",
        "/v3/api-docs",
        "/swagger-ui",
        "/swagger-ui.html"
    );

    // 앱 요청을 식별하는 헤더들
    private static final List<String> APP_HEADERS = Arrays.asList(
        "X-Client-Type",
        "X-App-Version",
        "X-Platform"
    );

    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) throws ServletException {
        String path = request.getRequestURI();
        
        // 제외할 경로들 확인
        for (String excludedPath : EXCLUDED_PATHS) {
            if (path.startsWith(excludedPath)) {
                return true;
            }
        }
        
        return false;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        String token = resolveToken(request);

        if (token != null && jwtTokenProvider.validateToken(token)) {
            Authentication auth = jwtTokenProvider.getAuthentication(token);
            SecurityContextHolder.getContext().setAuthentication(auth);
        }

        filterChain.doFilter(request, response);
    }

    private String resolveToken(HttpServletRequest request) {
        // 앱 요청인지 확인
        if (isAppRequest(request)) {
            // 앱 요청: Authorization 헤더만 사용
            return resolveTokenFromHeader(request);
        } else {
            // 웹 요청: Authorization 헤더 우선, 쿠키 차선
            String token = resolveTokenFromHeader(request);
            if (token == null) {
                token = resolveTokenFromCookie(request);
            }
            return token;
        }
    }

    private boolean isAppRequest(HttpServletRequest request) {
        // User-Agent로 모바일 앱 확인
        String userAgent = request.getHeader("User-Agent");
        if (userAgent != null && (userAgent.contains("Mobile") || userAgent.contains("Android") || userAgent.contains("iOS"))) {
            return true;
        }
        
        // 커스텀 헤더로 앱 요청 확인
        for (String header : APP_HEADERS) {
            if (request.getHeader(header) != null) {
                return true;
            }
        }
        
        // X-Requested-With 헤더로 AJAX 요청 확인 (웹에서도 사용 가능)
        String requestedWith = request.getHeader("X-Requested-With");
        if ("XMLHttpRequest".equals(requestedWith)) {
            return false; // 웹의 AJAX 요청
        }
        
        return false; // 기본적으로 웹 요청으로 간주
    }

    private String resolveTokenFromHeader(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (StringUtils.hasText(bearerToken) && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }

    private String resolveTokenFromCookie(HttpServletRequest request) {
        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("access_token".equals(cookie.getName())) {
                    return cookie.getValue();
                }
            }
        }
        return null;
    }
} 