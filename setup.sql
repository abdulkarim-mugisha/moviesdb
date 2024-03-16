-- A setup file for the movie review database.
--
-- Drop all tables if they exist.
DROP TABLE IF EXISTS follower;
DROP TABLE IF EXISTS movie_in_list;
DROP TABLE IF EXISTS list;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS movie_genre;
DROP TABLE IF EXISTS user_account;
DROP TABLE IF EXISTS movie;

-- Represents a movie in the database, uniquely identified by the movie_id.
CREATE TABLE movie (
    movie_id INT AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    description TEXT,
    director TEXT,
    cast TEXT,
    -- runtime of the movie in minutes
    runtime INT,
    PRIMARY KEY (movie_id)
);

-- A referencing relation to model a movie genre, uniquely identified by the 
-- movie_id and genre_name. 
CREATE TABLE movie_genre(
    movie_id INT,
    genre VARCHAR(20),
    PRIMARY KEY (movie_id, genre),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE
);

-- Represents a user in the database, uniquely identified by the user_id.
CREATE TABLE user_account (
    user_id INT AUTO_INCREMENT,
    username VARCHAR(255),
    salt CHAR(8),
    password_hash BINARY(64),
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bio TEXT,
    PRIMARY KEY (user_id),
    is_admin BOOLEAN DEFAULT FALSE
);

-- Represents a review in the database, uniquely identified by the user_id and
-- movie_id.
CREATE TABLE review (
    user_id INT,
    movie_id INT,
    rating NUMERIC(2, 1),
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES user_account(user_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
);

-- Represents a movie list in the database, uniquely identified by the list_id.
CREATE TABLE list (
    list_id INT AUTO_INCREMENT,
    created_by INT,
    title VARCHAR(255),
    description TEXT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (list_id),
    FOREIGN KEY (created_by) REFERENCES user_account(user_id)
);

-- A referencing relation to model a movie in a list, uniquely identified by the
-- list_id and movie_id.
CREATE TABLE movie_in_list (
    list_id INT,
    movie_id INT,
    PRIMARY KEY (list_id, movie_id),
    FOREIGN KEY (list_id) REFERENCES list(list_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
);

-- A referencing relation to model a follower, uniquely identified by the
-- user_id and following_id. 
CREATE TABLE follower (
    follower_id INT,
    following_id INT,
    PRIMARY KEY (follower_id, following_id),
    FOREIGN KEY (follower_id) REFERENCES user_account(user_id),
    FOREIGN KEY (following_id) REFERENCES user_account(user_id)
);

CREATE INDEX movie_title_idx ON movie(title);
CREATE INDEX movie_genre_idx ON movie_genre(genre);
