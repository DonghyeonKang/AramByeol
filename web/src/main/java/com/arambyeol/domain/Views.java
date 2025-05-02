package com.arambyeol.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "views")
@Getter @Setter
@NoArgsConstructor
public class Views {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(columnDefinition = "BIGINT DEFAULT 0")
    private Long views = 0L;
} 