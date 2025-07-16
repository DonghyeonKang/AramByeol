package com.arambyeol.service;

import lombok.RequiredArgsConstructor;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;
import java.util.Map;
import java.util.Random;
import java.util.concurrent.ConcurrentHashMap;

@Service
@RequiredArgsConstructor
public class EmailAuthService {
    private final JavaMailSender mailSender;
    // email -> (code, 만료시각) 저장
    private final Map<String, CodeWithExpiry> codeStore = new ConcurrentHashMap<>();
    private final Random random = new Random();
    private static final long EXPIRE_MILLIS = 5 * 60 * 1000; // 5분

    public void sendVerificationCode(String email) {
        String code = String.format("%06d", random.nextInt(1000000));
        long expiry = System.currentTimeMillis() + EXPIRE_MILLIS;
        codeStore.put(email, new CodeWithExpiry(code, expiry));

        // 실제 메일 발송
        SimpleMailMessage message = new SimpleMailMessage();
        message.setTo(email);
        message.setSubject("아람별 이메일 인증 코드");
        message.setText("아람별 인증코드: " + code + "\n5분 이내에 입력해 주세요.");
        mailSender.send(message);
    }

    public boolean verifyCode(String email, String code) {
        CodeWithExpiry entry = codeStore.get(email);
        if (entry == null) return false;
        if (System.currentTimeMillis() > entry.expiry) {
            codeStore.remove(email);
            return false; // 만료됨
        }
        return entry.code.equals(code);
    }

    private static class CodeWithExpiry {
        String code;
        long expiry;
        CodeWithExpiry(String code, long expiry) {
            this.code = code;
            this.expiry = expiry;
        }
    }
} 