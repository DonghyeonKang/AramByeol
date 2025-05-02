package com.arambyeol.repository;

import com.arambyeol.domain.Menu;
import com.arambyeol.domain.Review;
import com.arambyeol.domain.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface ReviewRepository extends JpaRepository<Review, Long> {
    @Query("SELECT r FROM Review r " +
           "JOIN FETCH r.menu m " +
           "WHERE r.user.userId = :userId")
    Page<Review> findByUserIdWithMenu(@Param("userId") Long userId, Pageable pageable);

    boolean existsByUserAndMenu(User user, Menu menu);
} 