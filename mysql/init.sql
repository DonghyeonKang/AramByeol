CREATE DATABASE IF NOT EXISTS arambyeol;
USE arambyeol;

-- 메뉴 테이블
CREATE TABLE IF NOT EXISTS menu (
    menu_id INT PRIMARY KEY AUTO_INCREMENT,
    menu VARCHAR(50) NOT NULL UNIQUE,
    img_path TEXT,
    CONSTRAINT menu_unique UNIQUE (menu)
);

-- 사용자 계정 테이블
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 조회수 테이블
CREATE TABLE IF NOT EXISTS views (
    id INT(10) PRIMARY KEY AUTO_INCREMENT,
    views BIGINT(5) DEFAULT 0
);

-- 식단표 테이블
CREATE TABLE IF NOT EXISTS plan (
    plan_id INT PRIMARY KEY AUTO_INCREMENT,
    menu_id INT NOT NULL,
    meal_type VARCHAR(10) NOT NULL,
    course VARCHAR(20) NOT NULL,
    date VARCHAR(10) NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id) ON DELETE CASCADE
);

-- 후기 테이블
CREATE TABLE IF NOT EXISTS review (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    menu_id INT NOT NULL,
    score INT(10) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id) ON DELETE CASCADE
);

-- 인덱스 생성
CREATE INDEX idx_menu_id ON plan(menu_id);
CREATE INDEX idx_user_review ON review(user_id);
CREATE INDEX idx_menu_review ON review(menu_id);
CREATE INDEX idx_menu_name ON menu(menu);
CREATE INDEX idx_username ON users(username);
CREATE INDEX idx_plan_date ON plan(date);

-- 기본 문자셋 설정
ALTER DATABASE arambyeol CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE menu CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE users CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE plan CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE review CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 필요한 다른 테이블들도 여기에 추가할 수 있습니다 