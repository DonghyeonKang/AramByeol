package com.arambyeol.controller;

import com.arambyeol.dto.ReviewRequestDto;
import com.arambyeol.dto.ReviewResponseDto;
import com.arambyeol.dto.PageResponseDto;
import com.arambyeol.service.ReviewService;
import com.arambyeol.security.CustomUserDetails;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@Tag(name = "Review", description = "리뷰 관련 API")
@RestController
@RequestMapping("/reviews")
@RequiredArgsConstructor
public class ReviewController {
    private final ReviewService reviewService;

    @Operation(summary = "내 리뷰 목록 조회", description = "사용자가 작성한 리뷰 목록을 페이지네이션과 함께 조회합니다.")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "리뷰 목록 조회 성공"),
        @ApiResponse(responseCode = "401", description = "인증되지 않은 사용자")
    })
    @GetMapping("/my")
    public ResponseEntity<PageResponseDto<ReviewResponseDto>> getMyReviews(
            @Parameter(description = "페이지 번호 (0부터 시작)", example = "0")
            @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "페이지 크기", example = "10")
            @RequestParam(defaultValue = "10") int size,
            @Parameter(description = "정렬 기준 (reviewId)", example = "reviewId")
            @RequestParam(defaultValue = "reviewId") String sort,
            @Parameter(description = "정렬 방향 (asc/desc)", example = "desc")
            @RequestParam(defaultValue = "desc") String direction,
            @AuthenticationPrincipal CustomUserDetails userDetails) {
        
        Sort.Direction sortDirection = Sort.Direction.fromString(direction);
        PageRequest pageRequest = PageRequest.of(page, size, Sort.by(sortDirection, sort));
        
        return ResponseEntity.ok(reviewService.getUserReviews(userDetails.getUserId(), pageRequest));
    }

    @Operation(summary = "리뷰 작성", description = "특정 메뉴에 대한 리뷰를 작성합니다.")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "리뷰 작성 성공"),
        @ApiResponse(responseCode = "400", description = "잘못된 요청"),
        @ApiResponse(responseCode = "401", description = "인증되지 않은 사용자"),
        @ApiResponse(responseCode = "409", description = "이미 리뷰가 존재함")
    })
    @PostMapping("/menus/{menuId}")
    public ResponseEntity<ReviewResponseDto> createReview(
            @Parameter(description = "메뉴 ID", example = "1")
            @PathVariable Integer menuId,
            @Valid @RequestBody ReviewRequestDto requestDto,
            @AuthenticationPrincipal CustomUserDetails userDetails) {
        return ResponseEntity.ok(reviewService.createReview(userDetails.getUserId(), menuId, requestDto));
    }

    @Operation(summary = "리뷰 수정", description = "작성한 리뷰를 수정합니다.")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "리뷰 수정 성공"),
        @ApiResponse(responseCode = "400", description = "잘못된 요청"),
        @ApiResponse(responseCode = "401", description = "인증되지 않은 사용자"),
        @ApiResponse(responseCode = "403", description = "리뷰 수정 권한 없음"),
        @ApiResponse(responseCode = "404", description = "리뷰를 찾을 수 없음")
    })
    @PutMapping("/{reviewId}")
    public ResponseEntity<ReviewResponseDto> updateReview(
            @Parameter(description = "리뷰 ID", example = "1")
            @PathVariable Long reviewId,
            @Valid @RequestBody ReviewRequestDto requestDto,
            @AuthenticationPrincipal CustomUserDetails userDetails) {
        return ResponseEntity.ok(reviewService.updateReview(userDetails.getUserId(), reviewId, requestDto));
    }
} 