package com.arambyeol.controller;

import com.arambyeol.service.ViewsService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Tag(name = "Views", description = "조회수 관련 API")
@RestController
@RequestMapping("/api/views")
@RequiredArgsConstructor
public class ViewsController {
    private final ViewsService viewsService;

    @Operation(summary = "조회수 조회", description = "특정 ID의 조회수를 조회합니다.")
    @GetMapping("/{id}")
    public ResponseEntity<Long> getViews(@PathVariable Long id) {
        return ResponseEntity.ok(viewsService.getViews(id));
    }
}