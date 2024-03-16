-- Loading data from CSV files into tables

DROP FUNCTION IF EXISTS make_salt;

DELIMITER !
CREATE FUNCTION make_salt(num_chars INT)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);

    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !
DELIMITER ;

LOAD DATA LOCAL INFILE 'data/movies.csv' INTO TABLE movie
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data/genres.csv' INTO TABLE movie_genre
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data/users.csv' INTO TABLE user_account 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(username, @password, is_admin)
SET salt = make_salt(8),
    password_hash = SHA2(CONCAT(salt, @password), 256);
    

LOAD DATA LOCAL INFILE 'data/lists.csv' INTO TABLE list
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(list_id,created_by,title,description);

LOAD DATA LOCAL INFILE 'data/movie_in_list.csv' INTO TABLE movie_in_list
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data/reviews.csv' INTO TABLE review
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(user_id,movie_id,rating,review_text);
