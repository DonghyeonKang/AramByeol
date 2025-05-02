package com.arambyeol.repository;

import com.arambyeol.domain.Menu;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.Optional;

public interface MenuRepository extends JpaRepository<Menu, Long> {
    @Query("SELECT m FROM Menu m LEFT JOIN FETCH m.reviews WHERE m.menuId = :menuId")
    Optional<Menu> findByIdWithReviews(@Param("menuId") Long menuId);
} 