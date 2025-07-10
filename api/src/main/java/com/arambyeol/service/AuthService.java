package com.arambyeol.service;

import com.arambyeol.domain.RefreshToken;
import com.arambyeol.domain.User;
import com.arambyeol.dto.LoginRequestDto;
import com.arambyeol.dto.UserRequestDto;
import com.arambyeol.dto.PasswordResetDto;
import com.arambyeol.dto.TokenResponseDto;
import com.arambyeol.repository.UserRepository;
import com.arambyeol.repository.RefreshTokenRepository;
import com.arambyeol.security.JwtTokenProvider;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class AuthService {
    private final UserRepository userRepository;
    private final RefreshTokenRepository refreshTokenRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;

    @Transactional
    public User register(UserRequestDto requestDto) {
        if (userRepository.existsByUsername(requestDto.getUsername())) {
            throw new IllegalArgumentException("이미 존재하는 사용자명입니다.");
        }

        User user = new User();
        user.setUsername(requestDto.getUsername());
        user.setPassword(passwordEncoder.encode(requestDto.getPassword()));
        return userRepository.save(user);
    }

    @Transactional
    public TokenResponseDto login(String username, String password) {
        User user = userRepository.findByUsername(username)
            .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 사용자입니다."));

        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new IllegalArgumentException("비밀번호가 일치하지 않습니다.");
        }

        // 기존 refresh token 삭제
        refreshTokenRepository.deleteByUser(user);

        // 새로운 토큰 생성
        String accessToken = jwtTokenProvider.createAccessToken(username);
        String refreshToken = jwtTokenProvider.createRefreshToken(username);

        // refresh token을 DB에 저장
        RefreshToken refreshTokenEntity = new RefreshToken();
        refreshTokenEntity.setToken(refreshToken);
        refreshTokenEntity.setUser(user);
        refreshTokenEntity.setExpiryDate(LocalDateTime.now().plusDays(7)); // 7일 후 만료
        refreshTokenRepository.save(refreshTokenEntity);

        return new TokenResponseDto(accessToken, refreshToken);
    }

    @Transactional(readOnly = true)
    public boolean checkUsernameDuplicate(String username) {
        return userRepository.existsByUsername(username);
    }

    @Transactional
    public void resetPassword(PasswordResetDto resetDto) {
        User user = userRepository.findByUsername(resetDto.getUsername())
            .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 사용자입니다."));

        user.setPassword(passwordEncoder.encode(resetDto.getNewPassword()));
        userRepository.save(user);
    }

    @Transactional
    public TokenResponseDto refreshAccessToken(String refreshToken) {
        if (!jwtTokenProvider.validateToken(refreshToken)) {
            throw new IllegalArgumentException("유효하지 않은 refresh token입니다.");
        }

        RefreshToken tokenEntity = refreshTokenRepository.findByToken(refreshToken)
            .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 refresh token입니다."));

        if (tokenEntity.isExpired()) {
            refreshTokenRepository.delete(tokenEntity);
            throw new IllegalArgumentException("만료된 refresh token입니다.");
        }

        String username = jwtTokenProvider.getUsername(refreshToken);
        String newAccessToken = jwtTokenProvider.createAccessToken(username);

        return new TokenResponseDto(newAccessToken, refreshToken);
    }

    @Transactional
    public void logout(String refreshToken) {
        refreshTokenRepository.findByToken(refreshToken)
            .ifPresent(refreshTokenRepository::delete);
    }
} 