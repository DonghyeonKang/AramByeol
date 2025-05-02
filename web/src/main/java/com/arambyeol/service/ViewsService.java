package com.arambyeol.service;

import com.arambyeol.domain.Views;
import com.arambyeol.repository.ViewsRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class ViewsService {
    private final ViewsRepository viewsRepository;

    @Transactional(readOnly = true)
    public Long getViews() {
        return viewsRepository.findById(1L)
                .map(Views::getViews)
                .orElse(0L);
    }

    @Transactional
    public void incrementViews() {
        // 해당 ID의 레코드가 없으면 생성
        if (!viewsRepository.existsById(1L)) {
            Views views = new Views();
            views.setId(1L);
            views.setViews(0L);
            viewsRepository.save(views);
        }
        viewsRepository.incrementViews(1L);
    }
} 