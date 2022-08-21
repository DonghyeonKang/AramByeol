----------------------------
---- 이상 없는 테이블
CREATE TABLE `week`(
    `day` varchar(2) NOT NULL PRIMARY KEY,
    `date` varchar(11) NOT NULL
);

CREATE TABLE `views` (
    `views` BIGINT(5)
);

INSERT INTO views(views) VALUE(0);

--------------------------------------------
---- 변경해야할 테이블
CREATE TABLE `menudata`(
    `id` INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `menu` varchar(50) UNIQUE,
    `score` INT(10),
    `reviewcount` INT(10)
);
CREATE TABLE `menudata`(
    `menu_id` INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `menu` varchar(50) UNIQUE,
    `score` INT(10),
    `reviewcount` INT(10)
);

CREATE TABLE `users` (
    `id` INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id` varchar(50) NOT NULL,
    `user_pw` TEXT NOT NULL
);

CREATE TABLE `review` (
    `user_id` varchar(50) NOT NULL,
    `menu` varchar(50) NOT NULL,
    `score` INT(10) NOT NULL
);

CREATE TABLE `dinner`(
    `day` varchar(2) NOT NULL,
    `cource` varchar(50),
    `menu` varchar(50) NOT NULL
);


CREATE TABLE `lunch`(
    `day` varchar(2) NOT NULL,
    `cource` varchar(50),
    `menu` varchar(50) NOT NULL
);

CREATE TABLE `morning`(
    `day` varchar(2) NOT NULL,
    `cource` varchar(50),
    `menu` varchar(50) NOT NULL
);

---- 아래로 변경
CREATE TABLE `menudata`(
    `menu_id` INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `menu` varchar(50) UNIQUE,
    `score`  FLOAT NOT NULL DEFAULT 0,
    `reviewcount` INT(10) NOT NULL DEFAULT 0
);

CREATE TABLE `users` (
    `user_id` varchar(320) NOT NULL UNIQUE PRIMARY KEY,
    `user_pw` TEXT NOT NULL,
    `nickname` TEXT NOT NULL
);

ALTER TABLE menudata DROP PRIMARY KEY;
ALTER TABLE menudata MODIFY COLUMN id INT(10) NOT NULL;
ALTER TABLE menudata DROP PRIMARY KEY;
ALTER TABLE menudata CHANGE COLUMN id menu_id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY;

ALTER TABLE users MODIFY COLUMN user_id VARCHAR(320);
ALTER TABLE users MODIFY COLUMN id INT(10) NOT NULL;
ALTER TABLE users DROP PRIMARY KEY;
ALTER TABLE users ADD PRIMARY KEY (user_id);
ALTER TABLE users DROP COLUMN id;
ALTER TABLE users ADD COLUMN `nickname` TEXT NOT NULL;

DROP TABLE review;
 
CREATE TABLE `review` (
    `user_id` varchar(320) NOT NULL,
    `menu_id` INT(10) NOT NULL UNIQUE,
    `score`  FLOAT NOT NULL DEFAULT 0,
    FOREIGN KEY (`user_id` ) REFERENCES `users`(`user_id`),
    FOREIGN KEY (`menu_id` ) REFERENCES `menudata`(`menu_id`)
);

DROP TABLE dinner;
CREATE TABLE `dinner`(
    `day` varchar(2) NOT NULL,
    `cource` varchar(50),
    `menu_id` INT(10) NOT NULL,
    FOREIGN KEY (`menu_id` ) REFERENCES `menudata`(`menu_id`)
);

DROP TABLE lunch;
CREATE TABLE `lunch`(
    `day` varchar(2) NOT NULL,
    `cource` varchar(50),
    `menu_id` INT(10) NOT NULL,
    FOREIGN KEY (`menu_id` ) REFERENCES `menudata`(`menu_id`)
);

DROP TABLE morning;
CREATE TABLE `morning`(
    `day` varchar(2) NOT NULL,
    `cource` varchar(50),
    `menu_id` INT(10) NOT NULL,
    FOREIGN KEY (`menu_id` ) REFERENCES `menudata`(`menu_id`)
);

-------------------------------
---- 추가해야할 테이블
CREATE TABLE `post` (
    `post_id` INT(10) PRIMARY KEY AUTO_INCREMENT,
    `user_id` VARCHAR(320) NOT NULL,
    `title` TEXT NOT NULL,
    `content` TEXT NOT NULL,
    `date` DATE NOT NULL,
    `category` TEXT NOT NULL,
    `score` INT NOT NULL,
    `meal_time` TEXT NOT NULL,
    `image` TEXT,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
);

CREATE TABLE `token` (
    `refresh_token` TEXT,
    `user_id` VARCHAR(320) NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
);

SELECT menudata.menu_id, menu, score, course
FROM menudata, morning, review
WHERE menudata.menu_id = morning.menu_id AND morning.menu_id = review.menu_id AND day='월';
