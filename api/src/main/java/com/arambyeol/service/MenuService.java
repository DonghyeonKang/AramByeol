package com.arambyeol.service;

import com.arambyeol.domain.Menu;
import com.arambyeol.domain.Review;
import com.arambyeol.dto.MenuScoreDto;
import com.arambyeol.repository.MenuRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.OptionalDouble;

@Service
@RequiredArgsConstructor
public class MenuService {
    private final MenuRepository menuRepository;

    @Transactional(readOnly = true)
    public double getAverageScore(Integer menuId) {
        Menu menu = menuRepository.findById(menuId)
                .orElseThrow(() -> new IllegalArgumentException("메뉴를 찾을 수 없습니다: " + menuId));

        OptionalDouble average = menu.getReviews().stream()
                .mapToInt(Review::getScore)
                .average();

        return average.orElse(0.0);
    }

    @Transactional(readOnly = true)
    public MenuScoreDto getMenuWithScore(Integer menuId) {
        Menu menu = menuRepository.findById(menuId)
                .orElseThrow(() -> new IllegalArgumentException("메뉴를 찾을 수 없습니다: " + menuId));

        double averageScore = menu.getReviews().stream()
                .mapToInt(Review::getScore)
                .average()
                .orElse(0.0);

        long reviewCount = menu.getReviews().size();

        return MenuScoreDto.builder()
                .menuId(menu.getMenuId())
                .menuName(menu.getMenu())
                .averageScore(averageScore)
                .reviewCount(reviewCount)
                .build();
    }
} 