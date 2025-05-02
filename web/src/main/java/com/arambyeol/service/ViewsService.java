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
    public Long getViews(Long id) {
        return viewsRepository.findById(id)
                .map(Views::getViews)
                .orElse(0L);
    }

    @Transactional
    public void incrementViews(Long id) {
        // 해당 ID의 레코드가 없으면 생성
        if (!viewsRepository.existsById(id)) {
            Views views = new Views();
            views.setId(id);
            views.setViews(0L);
            viewsRepository.save(views);
        }
        viewsRepository.incrementViews(id);
    }

    @Transactional(readOnly = true)
    public Views getViewsEntity(Long id) {
        return viewsRepository.findById(id)
                .orElseGet(() -> {
                    Views views = new Views();
                    views.setId(id);
                    views.setViews(0L);
                    return viewsRepository.save(views);
                });
    }
} 