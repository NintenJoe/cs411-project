-- A 'membership_entity' is either a user or a group.
DELIMITER ;

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS `membership_entity`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `group`;
DROP TABLE IF EXISTS `group_type`;
DROP TABLE IF EXISTS `group_membership`;

CREATE TABLE IF NOT EXISTS `membership_entity` (
  `id` INT PRIMARY KEY AUTO_INCREMENT
);

CREATE TABLE IF NOT EXISTS `user` (
  `id` INT PRIMARY KEY,
  `email` CHAR(255) UNIQUE NOT NULL,
  `name` CHAR(70) NOT NULL,
  `password` CHAR(40), -- users may not log on with NULL password
  `salt` CHAR(40) NOT NULL,
  `confirmed` BOOLEAN NOT NULL DEFAULT False,
  `confirmUUID` CHAR(36) UNIQUE NOT NULL,
  `refreshTok` CHAR(64),

  FOREIGN KEY (`id`)
  REFERENCES `membership_entity`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `group` (
  `id` INT PRIMARY KEY,
  `name` CHAR(70) NOT NULL,
  `description` TEXT,
  `type` INT NOT NULL,
  `maintainerId` INT,
  `academic_entity_id` INT,

  FOREIGN KEY (`id`)
  REFERENCES `membership_entity`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  
  FOREIGN KEY (`maintainerId`)
  REFERENCES `user` (`id`)
  ON DELETE SET NULL
  ON UPDATE CASCADE,

  FOREIGN KEY (`academic_entity_id`)
  REFERENCES `academic_entity`(`id`)
  ON DELETE RESTRICT
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
  ON UPDATE CASCADE,
  UNIQUE INDEX `idx_group_membership` (`group_id`, `member_id`)
);

SET foreign_key_checks = 1;
