package com.arambyeol.domain;

public enum MealType {
    BREAKFAST("아침"),
    LUNCH("점심"),
    DINNER("저녁");

    private final String description;

    MealType(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
} 