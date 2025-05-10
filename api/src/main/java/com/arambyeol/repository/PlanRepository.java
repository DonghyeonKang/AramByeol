package com.arambyeol.repository;

import com.arambyeol.domain.Plan;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

public interface PlanRepository extends JpaRepository<Plan, Long> {
    @Query("SELECT p FROM Plan p " +
           "LEFT JOIN FETCH p.menu m " +
           "LEFT JOIN FETCH m.reviews " +
           "WHERE p.date >= :today " +
           "ORDER BY p.date ASC, p.course ASC")
    List<Plan> findAllFuturePlansWithMenuAndReviews(@Param("today") String today);

    @Query("SELECT p FROM Plan p " +
           "LEFT JOIN FETCH p.menu m " +
           "LEFT JOIN FETCH m.reviews " +
           "WHERE p.date = :date " +
           "ORDER BY p.course ASC")
    List<Plan> findByDateWithMenuAndReviews(@Param("date") String date);
} 