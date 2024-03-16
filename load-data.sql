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

LOAD DATA LOCAL INFILE 'movies.csv' INTO TABLE movie
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
-- #TODO: May have to update the AUTO_INCREMENT variable

LOAD DATA LOCAL INFILE 'genres.csv' INTO TABLE movie_genre
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

-- #TODO: loading lists data

LOAD DATA LOCAL INFILE 'users.csv' INTO TABLE user_account 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(username, @password, is_admin)
SET password_hash = SHA2(CONCAT(salt, @password), 256), salt = make_salt(8);


