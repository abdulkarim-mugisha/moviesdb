-- Calculate the average rating of a specific movie by its movie_id
SELECT m.title, AVG(r.rating) AS average_rating
FROM movie m
LEFT JOIN review r ON m.movie_id = r.movie_id
WHERE m.movie_id = 1
GROUP BY m.title;

-- Get the top 10 movies ordered by their number of reviews, showing the 
-- movie id, title, release year, and review count
SELECT m.movie_id, 
       m.title, 
       EXTRACT(YEAR FROM m.release_date) AS release_year, 
       COUNT(r.movie_id) as review_count
FROM movie m
LEFT JOIN review r ON m.movie_id = r.movie_id
GROUP BY m.movie_id
ORDER BY review_count DESC
LIMIT 10;

-- Retrieve the first 10 action movies, showing their ID, title, and 
-- release year
SELECT m.movie_id, m.title, EXTRACT(YEAR FROM m.release_date) AS release_year
FROM movie m
JOIN movie_genre mg ON m.movie_id = mg.movie_id
WHERE mg.genre = 'Action'
LIMIT 10;

-- Find all movies released in 2018, ordered by release date
SELECT movie_id, title, EXTRACT(YEAR FROM release_date) AS release_year
FROM movie 
WHERE YEAR(release_date) = 2018
ORDER BY release_date DESC 
LIMIT 10;

-- Get the top 10 movies ordered by average rating (and then title for ties), 
-- showing their movie ID, title, and average rating
SELECT m.movie_id, m.title, AVG(r.rating) AS average_rating
FROM movie m
LEFT JOIN review r ON m.movie_id = r.movie_id
GROUP BY m.movie_id
ORDER BY average_rating DESC, m.title ASC 
LIMIT 10;  

-- Insert a new review into the review table
INSERT INTO review (user_id, movie_id, rating, review_text)
VALUES (1, 12, 4.5, 'Nice movie');

-- Create a new list with a title and description, associated with a specific 
-- user
INSERT INTO list (created_by, title, description)
VALUES (2, 'Edens watchlist', 'Can not wait to watch these');

-- Establish a following relationship between two users
INSERT INTO follower (follower_id, following_id)
VALUES (5, 8);

-- Add a movie to a specific list
INSERT INTO movie_in_list (list_id, movie_id)
VALUES (4, 9);

-- Remove a movie from a list
DELETE FROM movie_in_list WHERE list_id = 4 AND movie_id = 9;

-- Search for movies with titles that include the word 'Spider', showing their ID, title, and release year
SELECT movie_id, title, YEAR(release_date) AS release_year FROM movie WHERE title LIKE 'Spider';

-- Retrieve all details of a specific movie by its movie_id
SELECT * FROM movie WHERE movie_id = 1;

-- Get movies that are included in a specific list, showing their ID, title, and release year
SELECT m.movie_id, m.title, YEAR(release_date) AS release_year FROM movie m
JOIN movie_in_list mil ON m.movie_id = mil.movie_id
WHERE mil.list_id = 1;

-- Authenticate a user (placeholder for stored procedure call)
CALL authenticate('eden', 'edenpw');

-- Add a new user (placeholder for stored procedure call)
CALL sp_add_user('kwadwo', 'eagles$231', 'Love action packed movies', 0);

-- Retrieve all lists created by a specific user, showing their ID, title, 
-- description, and creation date
SELECT list_id, title, description, date_created FROM list
WHERE created_by = 1;

-- Retrieve all lists in the database, showing their ID, title, description,
--  and creation date
SELECT list_id, title, description, date_created FROM list;

-- Retrieve details of a list by its list_id 
SELECT * FROM list WHERE list_id = 1;

-- Retrieve details of a movie by its movie_id.
SELECT * FROM movie WHERE movie_id = 6;

-- Delete a specific movie from the database by its movie_id
DELETE FROM movie WHERE movie_id = 19;

-- Insert a new movie into the movie table with detailed information
INSERT INTO movie (title, release_date, description, director, cast, runtime)
VALUES 
('Ananse in the land of idiots', '2025-01-01', 
'The wise Ananse fools the people of the land of idiots and  
escapes with their Princess', 'Eden Obeng Kyei, Ama Ata Aidoo', 'Ananse', 100);

-- Delete a specific user account from the database by its user_id
DELETE FROM user_account WHERE user_id = 4;

-- Delete a specific list from the database by its list_id
DELETE FROM list WHERE list_id = 1;

