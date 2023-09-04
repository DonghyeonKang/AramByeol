CREATE TABLE `menudata`(
    `id` INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `menu` varchar(50) UNIQUE,
    `score` INT(10),
    `reviewcount` INT(10)
);

CREATE TABLE `dinner`(
    `day` varchar(2) NOT NULL,
    `course` varchar(50),
    `menu` varchar(50) NOT NULL
);


CREATE TABLE `lunch`(
    `day` varchar(2) NOT NULL,
    `course` varchar(50),
    `menu` varchar(50) NOT NULL
);

CREATE TABLE `morning`(
    `day` varchar(2) NOT NULL,
    `course` varchar(50),
    `menu` varchar(100) NOT NULL
);

CREATE TABLE `week`(
    `day` varchar(2) NOT NULL PRIMARY KEY, --키
    `date` varchar(11) NOT NULL --값
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