package com.arambyeol.controller;

import com.arambyeol.dto.PlanResponseDto;
import com.arambyeol.service.PlanService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Tag(name = "Plan", description = "식단표 관련 API")
@RestController
@RequestMapping("/api/plans")
@RequiredArgsConstructor
public class PlanController {
    private final PlanService planService;

    @Operation(summary = "향후 식단 조회", description = "오늘 이후의 모든 식단과 메뉴별 평균 평점을 조회합니다.")
    @GetMapping
    public ResponseEntity<List<PlanResponseDto>> getFuturePlans() {
        return ResponseEntity.ok(planService.getFuturePlans());
    }

    @Operation(summary = "특정 날짜 식단 조회", description = "지정된 날짜의 식단과 메뉴별 평균 평점을 조회합니다.")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "식단 조회 성공"),
        @ApiResponse(responseCode = "400", description = "잘못된 날짜 형식"),
        @ApiResponse(responseCode = "404", description = "해당 날짜의 식단이 없음")
    })
    @GetMapping("/{date}")
    public ResponseEntity<PlanResponseDto> getDailyPlan(
            @Parameter(description = "조회할 날짜 (형식: yyyy-MM-dd)", example = "2024-03-20")
            @PathVariable String date) {
        return ResponseEntity.ok(planService.getDailyPlan(date));
    }

    @Operation(summary = "주간 식단 조회", description = "지정된 날짜가 포함된 주의 전체 식단을 조회합니다.")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "주간 식단 조회 성공"),
        @ApiResponse(responseCode = "400", description = "잘못된 날짜 형식"),
        @ApiResponse(responseCode = "404", description = "해당 주의 식단이 없음")
    })
    @GetMapping("/weekly/{date}")
    public ResponseEntity<List<PlanResponseDto>> getWeeklyPlan(
            @Parameter(description = "조회할 기준 날짜 (형식: yyyy-MM-dd)", example = "2024-03-20")
            @PathVariable String date) {
        return ResponseEntity.ok(planService.getWeeklyPlan(date));
    }
} 