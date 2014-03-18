-- A 'membership_entity' is either a user or a group.
DELIMITER ;

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS `membership_entity`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `group`;
DROP TABLE IF EXISTS `group_type`;
DROP TABLE IF EXISTS `group_membership`;
SET foreign_key_checks = 1;

CREATE TABLE IF NOT EXISTS `membership_entity` (
  `id` INT PRIMARY KEY AUTO_INCREMENT
);

CREATE TABLE IF NOT EXISTS `user` (
  `id` INT UNIQUE NOT NULL,
  `email` CHAR(255) UNIQUE NOT NULL,
  `name` CHAR(70) NOT NULL,
  `password` CHAR(40), -- users may not log on with NULL password
  `salt` CHAR(40) NOT NULL,

  FOREIGN KEY (`id`)
  REFERENCES `membership_entity`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `group` (
  `id` INT UNIQUE NOT NULL,
  `name` CHAR(70) NOT NULL,
  `description` TEXT,
  `type` INT NOT NULL,

  FOREIGN KEY (`id`)
  REFERENCES `membership_entity`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `group_type` (
  `type_id` INT PRIMARY KEY,
  `type_name` CHAR(16)
);

CREATE TABLE IF NOT EXISTS `group_membership` (
  `group_id` INT NOT NULL,
  `member_id` INT NOT NULL,

  FOREIGN KEY (`group_id`)
  REFERENCES `group`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  FOREIGN KEY (`member_id`)
  REFERENCES `membership_entity`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE
)
