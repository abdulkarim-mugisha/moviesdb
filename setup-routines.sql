DROP FUNCTION IF EXISTS calc_movie_rating;

DELIMITER !
CREATE FUNCTION calc_movie_rating(movie_id INT) RETURNS DECIMAL(3,2)
DETERMINISTIC
BEGIN
    DECLARE avg_rating DECIMAL(3,2);
    SELECT AVG(r.rating) INTO avg_rating
    FROM movie m
    LEFT JOIN review r ON m.movie_id = r.movie_id
    WHERE m.movie_id = movie_id;
    RETURN IFNULL(avg_rating, 0.00);
END!
DELIMITER ;

DELIMITER !
CREATE PROCEDURE add_or_update_review(
    p_user_id INT,
    p_movie_id INT,
    p_rating NUMERIC(2, 1),
    p_review_text TEXT
)
BEGIN
    -- Check if a review already exists
    IF (SELECT COUNT(*) FROM review WHERE user_id = p_user_id AND movie_id = p_movie_id) > 0 THEN
        -- If the review exists, update it
        UPDATE review
        SET rating = p_rating,
            review_text = p_review_text,
            review_date = CURRENT_TIMESTAMP
        WHERE user_id = p_user_id AND movie_id = p_movie_id;
    ELSE
        -- If the review does not exist, insert it
        INSERT INTO review (user_id, movie_id, rating, review_text)
        VALUES (p_user_id, p_movie_id, p_rating, p_review_text);
    END IF;
END!
DELIMITER ;

DELIMITER //

CREATE PROCEDURE get_reviews_for_movie(IN p_movie_id INT)
BEGIN
    SELECT ua.username, r.rating, r.review_text
    FROM review r
    JOIN user_account ua ON r.user_id = ua.user_id
    WHERE r.movie_id = p_movie_id
    ORDER BY r.review_date DESC;
END //

DELIMITER ;

DELIMITER !
CREATE TRIGGER delete_empty_list
AFTER DELETE ON movie_in_list
FOR EACH ROW
BEGIN
    DECLARE remaining_movies INT;
    
    -- Count how many movies are still in the list
    SELECT COUNT(*) INTO remaining_movies
    FROM movie_in_list
    WHERE list_id = OLD.list_id;
    
    -- If no movies are left, delete the list
    IF remaining_movies = 0 THEN
        DELETE FROM list WHERE list_id = OLD.list_id;
    END IF;
END!
DELIMITER ;

DELIMITER !
CREATE PROCEDURE add_movie_to_list(p_list_id INT, p_movie_id INT)
BEGIN
    INSERT INTO movie_in_list (list_id, movie_id)
    VALUES (p_list_id, p_movie_id);
END !
DELIMITER ;


DELIMITER !
CREATE PROCEDURE remove_from_list(p_list_id INT, p_movie_id INT)
BEGIN
    DELETE FROM movie_in_list WHERE list_id = p_list_id AND movie_id = p_movie_id;
END !
DELIMITER ;


