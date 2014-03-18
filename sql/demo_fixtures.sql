-- hard-coded fixtures for demo purposes
DELIMITER ;

INSERT INTO `group_type` (`type_id`, `type_name`)
VALUES
(1, 'Academic');

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `user` (`id`, `email`, `name`, `password`, `salt`)
VALUES
(LAST_INSERT_ID(), 'josh@halstead.com', 'Josh Halstead', SHA1(CONCAT('b347c0caea913fcf2b7a868387295e390e649d01', 'unsecure')), 'b347c0caea913fcf2b7a868387295e390e649d01');

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `group` (`id`, `name`, `description`, `type`)
VALUES
(LAST_INSERT_ID(), 'CS 411 Database Systems', 'Examination of the logical organization of databases: the entity-relationship model; the hierarchical, network, and relational data models and their languages. Functional dependencies and normal forms. Design, implementation, and optimization of query languages; security and integrity; concurrency control, and distributed database systems.', 1);

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `group` (`id`, `name`, `description`, `type`)
VALUES
(LAST_INSERT_ID(), 'CS 418 Interactive Computer Graphics', 'Basic mathematical tools and computational techniques for modeling, rendering, and animating 3-D scenes.atabase systems.', 1);
