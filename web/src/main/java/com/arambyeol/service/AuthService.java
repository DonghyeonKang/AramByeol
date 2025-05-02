package com.arambyeol.service;

import com.arambyeol.domain.User;
import com.arambyeol.dto.LoginRequestDto;
import com.arambyeol.dto.UserRequestDto;
import com.arambyeol.dto.PasswordResetDto;
import com.arambyeol.repository.UserRepository;
import com.arambyeol.security.JwtTokenProvider;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class AuthService {
    private final UserRepository userRepository;
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

    @Transactional(readOnly = true)
    public String login(String username, String password) {
        User user = userRepository.findByUsername(username)
            .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 사용자입니다."));

        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new IllegalArgumentException("비밀번호가 일치하지 않습니다.");
        }

        return jwtTokenProvider.createToken(username);
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
} 