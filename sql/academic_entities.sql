DELIMITER ;

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS `academic_entity`;
DROP TABLE IF EXISTS `institution`;
DROP TABLE IF EXISTS `term`;
DROP TABLE IF EXISTS `course`;
DROP TABLE IF EXISTS `section`;
DROP TABLE IF EXISTS `class`;
SET foreign_key_checks = 1;

CREATE TABLE IF NOT EXISTS `academic_entity` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `type` ENUM('institution', 'term', 'course', 'section', 'class') NOT NULL,
  `group_id` INT,
  FOREIGN KEY (`group_id`)
  REFERENCES `group`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE
);

ALTER TABLE `group`
DROP FOREIGN KEY `fk_academic_entity`;
ALTER TABLE `group`
ADD CONSTRAINT `fk_academic_entity`
FOREIGN KEY (`academic_entity_id`)
REFERENCES `academic_entity`(`id`);

CREATE TABLE IF NOT EXISTS `institution` (
  `id` INT PRIMARY KEY,
  `name` CHAR(70) NOT NULL,

  FOREIGN KEY (`id`)
  REFERENCES `academic_entity`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `term` (
  `id` INT UNIQUE NOT NULL,
  -- institution
  `institution_id` INT NOT NULL,
  -- calendar year of the term start
  `year` YEAR NOT NULL,
  -- sequence index (e.g. 0 for Spring, 1 for Summer, 2 for Fall)
  -- the scheme may differ depending on the institution and year
  `sindex` TINYINT NOT NULL,
  -- human-readable term name e.g. Fall 2014
  `name` CHAR(32) NOT NULL,

  -- combinations of institution, year, and sequence index is the primary key
  PRIMARY KEY (`institution_id`, `year`, `sindex`),
  FOREIGN KEY (`institution_id`)
  REFERENCES `institution`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `course` (
  `id` INT PRIMARY KEY,
  `institution_id` INT NOT NULL,
  `term_id` INT NOT NULL,
  -- subject abbreviation e.g. CS
  `subject` CHAR(8) NOT NULL,
  -- course number e.g. 225
  `cnumber` CHAR(8) NOT NULL,
  -- human readable name e.g. CS 225
  `name` CHAR(18) NOT NULL,
  -- human readable title e.g. Data Structures
  `title` CHAR(48),

  FOREIGN KEY (`id`)
  REFERENCES `academic_entity`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  FOREIGN KEY (`institution_id`)
  REFERENCES `institution`(`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE,
  FOREIGN KEY (`term_id`)
  REFERENCES `term`(`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE,
  UNIQUE INDEX `idx_course` (`term_id`, `subject`, `cnumber`),
  UNIQUE INDEX `idx_course_name` (`term_id`, `name`)
);

CREATE TABLE IF NOT EXISTS `section` (
  `id` INT PRIMARY KEY,
  -- inst/term id is denormalized for indexing/search purposes
  `institution_id` INT NOT NULL,
  `term_id` INT NOT NULL,
  `course_id` INT NOT NULL,
  -- section number e.g. AL1
  `snumber` CHAR(8) NOT NULL,
  -- human readable title (useful for section-level classes)
  `title` CHAR(48),
  -- reference id (e.g. CRN of UIUC)
  `ref_id` CHAR(8),

  FOREIGN KEY (`id`)
  REFERENCES `academic_entity`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  FOREIGN KEY (`institution_id`)
  REFERENCES `institution`(`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE,
  UNIQUE INDEX `idx_ref_id` (`institution_id`, `term_id`, `ref_id`),
  UNIQUE INDEX `idx_unique_snumber` (`institution_id`, `term_id`, `course_id`, `snumber`)
);

-- realization of course/sections 
CREATE TABLE IF NOT EXISTS `class` (
  `id` INT PRIMARY KEY,
  `institution_id` INT NOT NULL,
  `term_id` INT NOT NULL,
  `course_id` INT NOT NULL,
  `name` CHAR(16) NOT NULL,
  `title` CHAR(48) NOT NULL,
  -- field for search e.g. 'CS 498 Prob for Comp Sci'
  `class_name` CHAR(66) NOT NULL,
  FOREIGN KEY (`id`)
  REFERENCES `academic_entity`(`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  FOREIGN KEY (`institution_id`)
  REFERENCES `institution`(`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE,
  FOREIGN KEY (`term_id`)
  REFERENCES `term`(`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE,
  FOREIGN KEY (`course_id`)
  REFERENCES `course`(`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE,
  UNIQUE INDEX `idx_class_search_name` (`term_id`, `class_name`, `name`, `title`),
  UNIQUE INDEX `idx_unique_class` (`course_id`, `title`)
);
