-- db table 의 스키마이다.
-- er-diagram 이 수정되어 스키마를 변경해야하면 이 파일도 수정해준다. 

CREATE TABLE `menudata`(
    `id` INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `menu` varchar(50) UNIQUE,
    `score` INT(10),
    `reviewcount` INT(10)
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

CREATE TABLE `week`(
    `day` varchar(2) NOT NULL PRIMARY KEY,
    `date` varchar(11) NOT NULL
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

CREATE TABLE `views` (
    `views` BIGINT(5)
);

INSERT INTO views(views) VALUE(0);