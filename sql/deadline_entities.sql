DELIMITER ;

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS `deadline`;
DROP TABLE IF EXISTS `deadline_metadata`;
SET foreign_key_checks = 1;

CREATE TABLE IF NOT EXISTS `deadline` (
  `id` INT PRIMARY KEY,
  `origin` INT,
  `deadline` DATETIME,

  FOREIGN KEY (`origin`)
  REFERENCES `deadline`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  INDEX `idx_deadline` (`deadline`)
);

CREATE TABLE IF NOT EXISTS `deadline_metadata` (
  `user_id` INT NOT NULL,
  `deadline_id` INT NOT NULL,
  `name` VARCHAR(64),
  `notes` TEXT,

  PRIMARY KEY (`user_id`, `deadline_id`),
  FOREIGN KEY (`user_id`)
  REFERENCES `user`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  FOREIGN KEY (`deadline_id`)
  REFERENCES `deadline`(`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE
);
