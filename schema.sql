CREATE TABLE `menudata` ( 
    `id` INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `menu` VARCHAR(50) UNIQUE,
    `score` INT(10),
    `reviewcount` INT(10)
);

CREATE TABLE `review`(
    `user_id` VARCHAR(50) NOT NULL,
    `menu` VARCHAR(50) NOT NULL, 
    `score` INT(10) NOT NULL
);

CREATE TABLE 'users'(
    `id` INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    `user_id` VARCHAR(50) NOT NULL, 
    `user_pw` VARCHAR(50) NOT NULL
);

CREATE TABLE `week`(
    `day` VARCHAR(2) NOT NULL primary key,
    `date` VARCHAR(11) NOT NULL
);

CREATE TABLE `morning`(
    `day` VARCHAR(2) NOT NULL,
    `cours` VARCHAR(50),
    `menu` VARCHAR(50) NOT NULL
);

CREATE TABLE `lunch`(
    `day` VARCHAR(2) NOT NULL,
    `course` VARCHAR(50),
    `menu` VARCHAR(50) NOT NULL
);

CREATE TABLE `dinner`(
    `day` VARCHAR(2) NOT NULL,
    `course` VARCHAR(50),
    `menu` VARCHAR(50) NOT NULL
);
