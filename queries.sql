SELECT m.title, AVG(r.rating) AS average_rating
FROM movie m
LEFT JOIN review r ON m.movie_id = r.movie_id
WHERE m.movie_id = 1
GROUP BY m.title;

SELECT m.movie_id, m.title, EXTRACT(YEAR FROM m.release_date), COUNT(r.movie_id) as review_count
FROM movie m
LEFT JOIN review r ON m.movie_id = r.movie_id
GROUP BY m.movie_id
ORDER BY review_count DESC
LIMIT 10;

SELECT m.movie_id, m.title, EXTRACT(YEAR FROM m.release_date)
FROM movie m
JOIN movie_genre mg ON m.movie_id = mg.movie_id
WHERE mg.genre = 'Action'
LIMIT 10;

SELECT movie_id, title, EXTRACT(YEAR FROM release_date) 
FROM movie 
WHERE YEAR(release_date) = 2018
ORDER BY title ASC 
LIMIT 10;

SELECT m.movie_id, m.title, AVG(r.rating) as average_rating
FROM movie m
LEFT JOIN review r ON m.movie_id = r.movie_id
GROUP BY m.movie_id
ORDER BY average_rating DESC, m.title ASC 
LIMIT 10;  

INSERT INTO review (user_id, movie_id, rating, review_text)
VALUES (1, 12, 4.5, 'Nice movie');

INSERT INTO list (created_by, title, description)
VALUES (2, 'Edens watchlist', 'Can not wait to watch these');

INSERT INTO follower (follower_id, following_id)
VALUES (5, 8);

INSERT INTO movie_in_list (list_id, movie_id)
VALUES (4, 9);

DELETE FROM movie_in_list WHERE list_id = 4 AND movie_id = 9;

SELECT movie_id, title, YEAR(release_date) FROM movie WHERE title LIKE 'Spider';

SELECT * FROM movie WHERE movie_id = 1;

SELECT m.movie_id, m.title, YEAR(release_date) FROM movie m
JOIN movie_in_list mil ON m.movie_id = mil.movie_id
WHERE mil.list_id = 1;

CALL authenticate('eden', 'edenpw');

CALL sp_add_user('kwadwo', 'eagles$231', 'Love action packed movies', 0);

SELECT list_id, title, description, date_created FROM list
WHERE created_by = 1;

SELECT list_id, title, description, date_created FROM list;

SELECT * FROM list WHERE list_id LIKE 1;

SELECT * FROM movie WHERE movie_id LIKE 6;

DELETE FROM movie WHERE movie_id = 19;

INSERT INTO movie (title, release_date, description, director, cast, runtime)
VALUES ('Ananse in the land of idiots', 2025, 'The wise Ananse fools the people of the land of idiots and  
escapes with their Princess', 'Eden Obeng Kyei, Ama Ata Aidoo', 'Ananse', 100);

DELETE FROM user_account WHERE user_id = 4;

DELETE FROM list WHERE list_id = 1;


