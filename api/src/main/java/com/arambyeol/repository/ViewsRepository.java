package com.arambyeol.repository;

import com.arambyeol.domain.Views;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;

public interface ViewsRepository extends JpaRepository<Views, Long> {
    @Modifying
    @Query("UPDATE Views v SET v.views = v.views + 1 WHERE v.id = :id")
    void incrementViews(Long id);
} 