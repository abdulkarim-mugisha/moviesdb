DROP FUNCTION IF EXISTS make_salt;
DROP FUNCTION IF EXISTS authenticate;
DROP PROCEDURE IF EXISTS sp_add_user;
DROP PROCEDURE IF EXISTS sp_change_password;

-- (Provided) This function generates a specified number of characters for using
-- as a salt in passwords.
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

-- Adds a new user to the user_info table, using the specified password (max
-- of 20 characters). Salts the password with a newly-generated salt value,
-- and then the salt and hash values are both stored in the table.
DELIMITER !
CREATE PROCEDURE sp_add_user(new_username VARCHAR(20), password VARCHAR(20), is_admin BOOLEAN)
BEGIN
  DECLARE salt CHAR(8);
  DECLARE password_hash BINARY(64);

  SET salt = make_salt(8);
  SET password_hash = SHA2(CONCAT(salt, password), 256);

  INSERT INTO user_account(username, salt, password_hash, is_admin) VALUES 
    (new_username, salt, password_hash, is_admin);
END !
DELIMITER ;

-- Authenticates the specified username and password against the data
-- in the user_info table.  Returns 1 if the user appears in the table, and the
-- specified password hashes to the value for the user. Otherwise returns 0.
DELIMITER !
CREATE FUNCTION authenticate(username VARCHAR(20), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
  IF EXISTS 
    (
      SELECT * FROM user_account U
      WHERE U.username = username 
      AND U.password_hash = SHA2(CONCAT(U.salt, password), 256)
    ) THEN RETURN 1;
  ELSE
    RETURN 0;
  END IF;

END !
DELIMITER ;

-- Changes the given user's password to the given password 
-- (after salting and hashing)
DELIMITER !
CREATE PROCEDURE sp_change_password(
  username VARCHAR(20), 
  new_password VARCHAR(20)
)
BEGIN 
  DECLARE new_salt CHAR(8);
  DECLARE new_password_hash BINARY(64);

  SET new_salt = make_salt(8);
  SET new_password_hash = SHA2(CONCAT(new_salt, new_password), 256);

  UPDATE user_account U
  SET U.salt = new_salt,
      U.password_hash = new_password_hash 
  WHERE U.username = username;  
END !
DELIMITER ;
