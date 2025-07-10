package com.arambyeol.service;

import com.arambyeol.domain.Menu;
import com.arambyeol.domain.Review;
import com.arambyeol.domain.User;
import com.arambyeol.dto.ReviewRequestDto;
import com.arambyeol.dto.ReviewResponseDto;
import com.arambyeol.dto.PageResponseDto;
import com.arambyeol.repository.MenuRepository;
import com.arambyeol.repository.ReviewRepository;
import com.arambyeol.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ReviewService {
    private final ReviewRepository reviewRepository;
    private final UserRepository userRepository;
    private final MenuRepository menuRepository;

    @Transactional(readOnly = true)
    public PageResponseDto<ReviewResponseDto> getUserReviews(Integer userId, Pageable pageable) {
        Page<Review> reviewPage = reviewRepository.findByUserIdWithMenu(userId, pageable);

        List<ReviewResponseDto> reviews = reviewPage.getContent().stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());

        return PageResponseDto.<ReviewResponseDto>builder()
                .content(reviews)
                .pageNumber(reviewPage.getNumber())
                .pageSize(reviewPage.getSize())
                .totalElements(reviewPage.getTotalElements())
                .totalPages(reviewPage.getTotalPages())
                .hasNext(reviewPage.hasNext())
                .hasPrevious(reviewPage.hasPrevious())
                .build();
    }

    private ReviewResponseDto convertToDto(Review review) {
        return ReviewResponseDto.builder()
                .reviewId(review.getReviewId())
                .menuId(review.getMenu().getMenuId())
                .username(review.getUser().getUsername())
                .menuName(review.getMenu().getMenu())
                .imgPath(review.getMenu().getImgPath())
                .score(review.getScore())
                .build();
    }

    @Transactional
    public ReviewResponseDto createReview(Integer userId, Integer menuId, ReviewRequestDto requestDto) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("사용자를 찾을 수 없습니다: " + userId));
        
        Menu menu = menuRepository.findById(menuId)
                .orElseThrow(() -> new IllegalArgumentException("메뉴를 찾을 수 없습니다: " + menuId));

        // 이미 리뷰를 작성했는지 확인
        if (reviewRepository.existsByUserAndMenu(user, menu)) {
            throw new IllegalStateException("이미 해당 메뉴에 대한 리뷰를 작성했습니다.");
        }

        Review review = Review.builder()
                .user(user)
                .menu(menu)
                .score(requestDto.getScore())
                .build();

        Review savedReview = reviewRepository.save(review);
        return convertToDto(savedReview);
    }

    @Transactional
    public ReviewResponseDto updateReview(Integer userId, Long reviewId, ReviewRequestDto requestDto) {
        Review review = reviewRepository.findById(reviewId)
                .orElseThrow(() -> new IllegalArgumentException("리뷰를 찾을 수 없습니다: " + reviewId));

        // 리뷰 작성자 확인
        if (!review.getUser().getUserId().equals(userId)) {
            throw new IllegalStateException("리뷰를 수정할 권한이 없습니다.");
        }

        review.setScore(requestDto.getScore());
        return convertToDto(review);
    }
} 