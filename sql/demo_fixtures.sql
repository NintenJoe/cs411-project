-- hard-coded fixtures for demo purposes
DELIMITER ;

INSERT INTO `group_type` (`type_id`, `type_name`)
VALUES
(1, 'Academic');

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `group` (`id`, `name`, `description`, `type`)
VALUES
(LAST_INSERT_ID(), 'UIUC', 'Illinois', 1);

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `user` (`id`, `email`, `name`, `password`, `salt`, `confirmUUID`)
VALUES
(LAST_INSERT_ID(), 'josh@halstead.com', 'Josh Halstead', SHA1(CONCAT('b347c0caea913fcf2b7a868387295e390e649d01', 'unsecure')), 'b347c0caea913fcf2b7a868387295e390e649d01', 'a');

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `user` (`id`, `email`, `name`, `password`, `salt`, `confirmUUID`)
VALUES
(LAST_INSERT_ID(), 'joe@ciurej.com', 'Joe Ciurej', SHA1(CONCAT('1b347c0caea913fcf2b7a868387295e390e649d0', 'unsecure')), '1b347c0caea913fcf2b7a868387295e390e649d0', 'b');

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `user` (`id`, `email`, `name`, `password`, `salt`, `confirmUUID`)
VALUES
(LAST_INSERT_ID(), 'eunsoo@roh.com', 'Eunsoo Roh', SHA1(CONCAT('47c0caea913fcf2b7a868387295e390e649d01b3', 'unsecure')), '47c0caea913fcf2b7a868387295e390e649d01b3', 'c');

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `user` (`id`, `email`, `name`, `password`, `salt`, `confirmUUID`)
VALUES
(LAST_INSERT_ID(), 'kyle@nusbaum.com', 'Kyle Nusbaum', SHA1(CONCAT('7c0caea913fcf2b7a868387295e390e649d01b34', 'unsecure')), '7c0caea913fcf2b7a868387295e390e649d01b34', 'd');

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `user` (`id`, `email`, `name`, `password`, `salt`, `confirmUUID`)
VALUES
(LAST_INSERT_ID(), 'tom@bogue.com', 'Tom Bogue', SHA1(CONCAT('c0caea913fcf2b7a868387295e390e649d01b347', 'unsecure')), 'c0caea913fcf2b7a868387295e390e649d01b347', 'e');

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `user` (`id`, `email`, `name`, `password`, `salt`, `confirmUUID`)
VALUES
(LAST_INSERT_ID(), 'lumen@faey.com', 'Lumen Faey', SHA1(CONCAT('0caea913fcf2b7a868387295e390e649d01b347c', 'unsecure')), '0caea913fcf2b7a868387295e390e649d01b347c', 'f');

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `group` (`id`, `name`, `description`, `type`)
VALUES
(LAST_INSERT_ID(), 'CS 411 Database Systems', 'Examination of the logical organization of databases: the entity-relationship model; the hierarchical, network, and relational data models and their languages. Functional dependencies and normal forms. Design, implementation, and optimization of query languages; security and integrity; concurrency control, and distributed database systems.', 1);

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `group` (`id`, `name`, `description`, `type`)
VALUES
(LAST_INSERT_ID(), 'CS 418 Interactive Computer Graphics', 'Basic mathematical tools and computational techniques for modeling, rendering, and animating 3-D scenes.database systems.', 1);

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `group` (`id`, `name`, `description`, `type`)
VALUES
(LAST_INSERT_ID(), 'CS 421 Programing Languages and Compilers', 'Structure of programming languages and their implementation. Basic language design principles; abstract data types; functional languages; type systems; object-oriented languages. Basics of lexing, parsing, syntax-directed translation, semantic analysis, and code generation.', 1);

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `group` (`id`, `name`, `description`, `type`)
VALUES
(LAST_INSERT_ID(), 'CS 473 Fundamental Algorithms', 'Fundamental techniques for algorithm design and analysis, including recursion, dynamic programming, randomization, dynamic data structures, fundamental graph algorithms, and NP-completeness. Intended for undergraduates in Computer Science and graduate students in other departments.', 1);

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `group` (`id`, `name`, `description`, `type`)
VALUES
(LAST_INSERT_ID(), 'CS 473 Study Team', 'Do Homework and learn to be smart!', 1);

INSERT INTO `membership_entity` VALUES ();
INSERT INTO `group` (`id`, `name`, `description`, `type`)
VALUES
(LAST_INSERT_ID(), 'CS 411 Project Team', 'Work together on the CS 411 project!', 1);


SET @group_id = (SELECT id FROM `group` WHERE name = 'UIUC');

SET @user_id = (SELECT id FROM user WHERE email = 'josh@halstead.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'joe@ciurej.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'eunsoo@roh.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'kyle@nusbaum.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'tom@bogue.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'lumen@faey.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM `group` WHERE name = 'CS 411 Database Systems');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM `group` WHERE name = 'CS 418 Interactive Computer Graphics');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM `group` WHERE name = 'CS 421 Programing Languages and Compilers');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM `group` WHERE name = 'CS 473 Fundamental Algorithms');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);


SET @group_id = (SELECT id FROM `group` WHERE name = 'CS 411 Database Systems');

SET @user_id = (SELECT id FROM user WHERE email = 'josh@halstead.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'joe@ciurej.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'eunsoo@roh.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'kyle@nusbaum.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'tom@bogue.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'lumen@faey.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM `group` WHERE name = 'CS 411 Project Team');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);

SET @group_id = (SELECT id FROM `group` WHERE name = 'CS 411 Project Team');

SET @user_id = (SELECT id FROM user WHERE email = 'josh@halstead.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'joe@ciurej.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'eunsoo@roh.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'kyle@nusbaum.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'tom@bogue.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);

SET @group_id = (SELECT id FROM `group` WHERE name = 'CS 418 Interactive Computer Graphics');

INSERT INTO `deadline` (`name`, group_id, deadline, `type`)
VALUES ('HW 1 (END)', @group_id, NOW(), 'END');
SET @end_id = (SELECT id FROM `deadline` WHERE `name` = 'HW 1 (END)');

INSERT INTO `deadline` (`name`, group_id, deadline, `type`)
VALUES ('HW 2 (COM)', @group_id, NOW(), 'COM');
SET @com_id = (SELECT id FROM `deadline` WHERE `name` = 'HW 2 (COM)');

INSERT INTO `deadline` (`name`, group_id, deadline, `type`)
VALUES ('HW 3 (PER)', @group_id, NOW(), 'PER');
SET @per_id = (SELECT id FROM `deadline` WHERE `name` = 'HW 3 (PER)');

SET @user_id = (SELECT id FROM user WHERE email = 'josh@halstead.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);

INSERT INTO `deadline_metadata`
VALUES (@user_id, @end_id, 'Josh Endorsed Deadline Notes');

INSERT INTO `deadline_metadata`
VALUES (@user_id, @com_id, 'Josh Communal Deadline Notes');

INSERT INTO `deadline_metadata`
VALUES (@user_id, @per_id, 'Josh Personal Deadline Notes');

SET @user_id = (SELECT id FROM user WHERE email = 'eunsoo@roh.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);

INSERT INTO `deadline_metadata`
VALUES (@user_id, @end_id, 'Eunsoo  Endorsed Deadline Notes');

INSERT INTO `deadline_metadata`
VALUES (@user_id, @com_id, 'Eunsoo Communal Deadline Notes');

SET @user_id = (SELECT id FROM user WHERE email = 'kyle@nusbaum.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);

SET @group_id = (SELECT id FROM `group` WHERE name = 'CS 421 Programing Languages and Compilers');

SET @user_id = (SELECT id FROM user WHERE email = 'kyle@nusbaum.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);

SET @group_id = (SELECT id FROM `group` WHERE name = 'CS 473 Fundamental Algorithms');

SET @user_id = (SELECT id FROM user WHERE email = 'josh@halstead.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'joe@ciurej.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'eunsoo@roh.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'tom@bogue.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'lumen@faey.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM `group` WHERE name = 'CS 473 Study Team');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);

SET @group_id = (SELECT id FROM `group` WHERE name = 'CS 473 Study Team');



SET @user_id = (SELECT id FROM user WHERE email = 'josh@halstead.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'tom@bogue.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);
SET @user_id = (SELECT id FROM user WHERE email = 'lumen@faey.com');
INSERT INTO `group_membership` VALUES (@group_id, @user_id);

