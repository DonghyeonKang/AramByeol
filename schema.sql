CREATE TABLE `menuData`(
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `menu` TEXT,
    `star` INT
);

CREATE TABLE `dinner`(
    `day` TEXT NOT NULL,
    `cource` TEXT,
    `menu` TEXT NOT NULL
);

CREATE TABLE `lunch`(
    `day` TEXT NOT NULL,
    `cource` TEXT,
    `menu` TEXT NOT NULL

);

CREATE TABLE `morning`(
    `day` TEXT NOT NULL,
    `cource` TEXT,
    `menu` TEXT NOT NULL
);

CREATE TABLE `week`(
    `day` TEXT NOT NULL,
    `date` DATE NOT NULL
);

CREATE TABLE `users` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `username` TEXT NOT NULL,
    `password` TEXT NOT NULL
);

CREATE TABLE `review` (
    `identify` TEXT NOT NULL,
    `menu` TEXT NOT NULL,
    `star` INT NOT NULL
);