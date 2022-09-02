CREATE TABLE `week`(
    `day` varchar(2) NOT NULL PRIMARY KEY,
    `date` varchar(11) NOT NULL
);

CREATE TABLE `views` (
    `views` BIGINT(5) NOT NULL DEFAULT 0
);

CREATE TABLE `menudata`(
    `menu_id` INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `menu` varchar(50) UNIQUE,
    `score`  FLOAT NOT NULL DEFAULT 0,
    `reviewcount` INT(10) NOT NULL DEFAULT 0
);

CREATE TABLE `morning`(
    `day` varchar(2) NOT NULL,
    `cource` varchar(50),
    `menu_id` INT(10) NOT NULL,
    FOREIGN KEY (`menu_id` ) REFERENCES `menudata`(`menu_id`)
);

CREATE TABLE `lunch`(
    `day` varchar(2) NOT NULL,
    `cource` varchar(50),
    `menu_id` INT(10) NOT NULL,
    FOREIGN KEY (`menu_id` ) REFERENCES `menudata`(`menu_id`)
);

CREATE TABLE `dinner`(
    `day` varchar(2) NOT NULL,
    `cource` varchar(50),
    `menu_id` INT(10) NOT NULL,
    FOREIGN KEY (`menu_id` ) REFERENCES `menudata`(`menu_id`)
);

CREATE TABLE `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` varchar(320) NOT NULL,
    `user_pw` TEXT NOT NULL,
    `nickname` TEXT NOT NULL,
    `verifing` INT DEFAULT 0
);
 
CREATE TABLE `review` (
    `uid` INT NOT NULL,
    `menu_id` INT(10) NOT NULL UNIQUE,
    `score`  FLOAT NOT NULL DEFAULT 0,
    FOREIGN KEY (`uid` ) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`menu_id` ) REFERENCES `menudata`(`menu_id`)
);

CREATE TABLE `post` (
    `post_id` INT(10) PRIMARY KEY AUTO_INCREMENT,
    `uid` INT NOT NULL,
    `title` TEXT NOT NULL,
    `content` TEXT NOT NULL,
    `date` DATE NOT NULL,
    `category` TEXT NOT NULL,
    `score` INT NOT NULL,
    `meal_time` TEXT NOT NULL,
    `image` TEXT,
    FOREIGN KEY (`uid`) REFERENCES `users`(`id`) ON DELETE CASCADE
);

CREATE TABLE `token` (
    `refresh_token` TEXT,
    `user_id` VARCHAR(320) NOT NULL
);

CREATE TABLE `mail` (
    `user_id` VARCHAR(320) NOT NULL,
    `token` TEXT NOT NULL
);
