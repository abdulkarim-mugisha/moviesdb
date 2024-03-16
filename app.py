"""
Student name(s): Eden Obeng Kyei, Abdulkarim Mugisha
Student email(s): eobengky@caltech.edu, amugisha@caltech.edu
We propose a social movies and tv-shows application, where users maintain 
movie lists, and can review movies on a 5-star scale. The program will allow 
the users to write reviews of movies and also read the reviews of other members
in the database. The users can also rate the movies after reading them and the 
average rating of the movie would be the average of all the ratings from the users. 
The users also get to like their favorite movies, actors/ actresses, directors, 
and producers, and can follow groups and friends. 
"""

import sys  # to print error messages to sys.stderr
import mysql.connector
from simple_term_menu import TerminalMenu

# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode
from datetime import datetime


# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = True


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """ "
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="appadmin",
            # Find port in MAMP or MySQL Workbench GUI or with
            # SHOW VARIABLES WHERE variable_name LIKE 'port';
            port="3306",  # this may change!
            password="adminpw",
            database="moviedb",  # replace this with your database name
        )
        print("Successfully connected.")
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr("Incorrect username or password when connecting to DB.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr("Database does not exist.")
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr("An error occurred, please contact the administrator.")
        sys.exit(1)


# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def find_movie_rating(movie_id):
    """
    Calculates the average rating of a movie.
    """
    sql = f"""
    SELECT m.title, AVG(r.rating) AS average_rating
    FROM movie m
    LEFT JOIN review r ON m.movie_id = r.movie_id
    WHERE m.movie_id = {movie_id}
    GROUP BY m.title;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when finding the movie rating.")
            return
    return rows[0]


def view_movies_by_popularity():
    """
    Provides a list of the most popular movies.
    """
    cursor = conn.cursor()
    sql = """
    SELECT m.title, COUNT(r.movie_id) as review_count
    FROM movie m
    LEFT JOIN review r ON m.movie_id = r.movie_id
    GROUP BY m.movie_id
    ORDER BY review_count DESC;
    """
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr(
                "An error occurred when trying to provide a list \
                of the most popular movies"
            )
            return
    if not rows:
        print("No results found.")
    else:
        print("Here are the most popular movies: \n")
        for row in rows:
            print(row)


def view_movies_by_genre():
    """
    Provides a list of all the movies of a given genre
    """
    genre = input("Enter the genre: ")
    cursor = conn.cursor()
    sql = f"""
    SELECT m.title
    FROM movie m
    JOIN movie_genre mg ON m.movie_id = mg.movie_id
    WHERE mg.genre = {genre}
    ORDER BY m.title ASC;
    """
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr(
                "An error occurred when generating movies of the genre: {}".format(
                    genre
                )
            )
            return
    if not rows:
        print("No movies found in the genre: {}.".format(genre))
    else:
        print("Here are the movie in the genre {}: \n".format(genre))
        for row in rows:
            print(row)


def view_movies_by_year():
    """
    Provides a list of all the movies released in a given year
    """
    year = input("Please enter the release year: ")
    cursor = conn.cursor()
    sql = (
        "SELECT title, release_date FROM movie WHERE YEAR(release_date) = %s ORDER BY title ASC;"
        % (year)
    )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr(
                "An error occurred when generating movies released in {}.".format(year)
            )
            return
    if not rows:
        print("No movies found for this {}".format(year))
    else:
        print("Here are the movies released in {}: \n".format(year))
        for row in rows:
            print(row)


def view_movies_by_rating():
    """
    Provides a list of the movies ordered by rating.
    """
    cursor = conn.cursor()
    sql = """
    SELECT m.title, AVG(r.rating) as average_rating
    FROM movie m
    LEFT JOIN review r ON m.movie_id = r.movie_id
    GROUP BY m.title
    ORDER BY average_rating DESC, m.title ASC;  
    """
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr(
                "An error occurred when generating movies with the highest \
                rating."
            )
            return
    if not rows:
        print("No results found.")
    else:
        print("Here are the movies with the highest rating: \n")
        for row in rows:
            print(row)
            # title, average_rating = row  # Tuple unpacking
            # print(f"{title}: {average_rating if average_rating is not None else 'Not rated'}")


def write_a_review(user_id, movie_id):
    """
    Writes a review for a movie. Prompts the user for their user ID, the movie ID,
    their rating, and their review text, then inserts this information into the reviews table.
    """
    rating = input("Please rate the movie (0.0 to 5.0): ")
    new_review = input("Write your review: ")
    review_date = datetime.now().strftime("%Y-%m-%d")
    sql = """
    INSERT INTO review (user_id, movie_id, rating, review_text, review_date)
    VALUES (%s, %s, %s, %s, %s);
    """ % (
        user_id,
        movie_id,
        rating,
        new_review,
        review_date,
    )
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        print("Your review has been successfully submitted.")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when writing a review for the movie")
            return


def create_list(user_id):
    """
    Creates a list of movies.
    """
    title = input("Please enter the title of your new list: ")
    description = input("Please enter a description for your new list: ")
    cursor = conn.cursor()
    sql = """
    INSERT INTO list (user_id, title, description)
    VALUES (%s, %s, %s, %s);
    """ % (
        user_id,
        title,
        description
    )
    try:
        cursor.execute(sql)
        print("Your new list has been successfully created.")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when creating your new list.")
            return


def follow_a_user(follower_id, following_id):
    """
    Follows a user
    """
    cursor = conn.cursor()
    sql = """
    INSERT INTO follower (follower_id, following_id)
    VALUES (%s, %s);
    """ % (
        follower_id,
        following_id,
    )
    try:
        cursor.execute(sql)
        print("You are now following the user.")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when trying to follower the user.")
            return


def add_movie_to_list(list_id, movie_id):
    """
    Adds a movie to a user's list by inserting a record into the list_movies table.
    """
    cursor = conn.cursor()
    sql = """
    INSERT INTO movie_in_list (list_id, movie_id)
    VALUES (%s, %s);
    """ % (
        list_id,
        movie_id,
    )
    try:
        cursor.execute(sql)
        print("The movie has been successfully added to your list.")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when adding the movie to the list.")
            return


def remove_movie_from_list(list_id, movie_id):
    """
    Removes a movie from a user's list by deleting the record from the list_movies table.
    """
    cursor = conn.cursor()
    sql = """
    DELETE FROM movie_in_list WHERE list_id = %s AND movie_id = %s;
    """ % (
        list_id,
        movie_id,
    )
    try:
        cursor.execute(sql)
        if cursor.rowcount > 0:
            print("The movie has been successfully removed from your list.")
        else:
            print("The movie was not found in the specified list.")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when removing the movie from the list.")
            return

def search_movies_by_name(query):
    cursor = conn.cursor()
    sql = """
    SELECT * FROM movie WHERE title LIKE %s;
    """ % (
        query,
    )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when searching for movies by name.")
            return
    return rows

def search_movies_by_id(query):
    cursor = conn.cursor()
    sql = """
    SELECT * FROM movie WHERE movie_id = %s;
    """ % (
        query,
    )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when searching for movies by id.")
            return
    return rows


def get_movies_in_list(list_id):
    #TODO: define function for retrieving movie list from list_id
    # return a movie dict containing id and other info
    
    pass

    
    

# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_lists_menu():
    pass

def show_movie_details(movie_id, movie_title, run_time, release_date, genre, description):
    movie_rating = find_movie_rating(movie_id)
    print("Title: %s" % movie_title)
    print("Release Date: %s" % release_date)
    print("Genre: %s" % genre)
    print("Description: %s" % description)
    print("What would you like to do? ")
    print("     (r - write a review")
    print("     (a - add to watch list")
    print("     (q) - quit")
    while True:
        ans = input("Enter an option: ")[0].lower()
        if ans == "r":
            # write_a_review(user_id, movie_id) 
            pass
        elif ans == "a":
            # add_movie_to_list()
            pass
        elif ans == "q":
            quit_ui()
        else:
            print("Unknown option.")
    
def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print("Good bye!")
    exit()

def display_results(movies):
    pass


def show_movie_search_menu():
    query = input("Enter movie title: ")
    # movies = search_movies_by_name(query)
    # display_results(movies)
    
def show_movies_menu():
    options = [
        "View movies by popularity",
        "View movies by genre",
        "View movies by rating",
        "View movies by year",
        "Search for a Movie",
        "Go back"
    ]
    movies_menu = TerminalMenu(options,
                               title="Movies")

    choice = movies_menu.show()
    if choice == 0:
        view_movies_by_popularity()
    elif choice == 1:
        view_movies_by_genre()
    elif choice == 2:
        view_movies_by_rating()
    elif choice == 3:
        view_movies_by_year()
    elif choice == 4:
        show_movie_search_menu()
    elif choice == 5:
        show_main_menu()

    
def show_lists_menu():
    options = [
        "My Lists",
        "Followed Lists"
        "All lists",
        "Create List",
        "Go back"
    ]
    lists_menu = TerminalMenu(options,
                               title="Lists")
    choice = lists_menu.show()
    if choice == 0:
        # show_my_lists()
        pass
    elif choice == 1:
        # show followed lists
        pass
    elif choice == 2:
        # show_all_lists()
        pass
    elif choice == 3:
        # create_list()
        pass
    elif choice == 4:
        show_main_menu()


def show_my_lists():
    pass

def show_all_lists():
    pass

def create_list():
    pass

def get_list_title(list_id):
    pass

def show_movie_details(movie, list_id=None): 
    options = [
        'Save to List',
        'Write a Review',
        'Rate Movie'
    ]
    if list_id:
        options.append("Remove from List")
    #TODO: implementing the movie view 

def show_list(list_id):
    movies = get_movies_in_list(list_id)
    movies_list = [f"{movie['title']} {movie['year']}" for movie in movies]
    list_title = get_list_title(list_id)
    list_menu = TerminalMenu(movies_list,
                             title = f"List: {list_title}")
    choice = list_menu.show() 
    show_movie_details(movies[choice], list_id=list_id)
    
    

def show_main_menu():
    options = [
        "Browse Movies",
        "Browse Movie Lists",
        "My Watchlist", 
        "Quit"
    ]
    main_menu = TerminalMenu(options, 
                             title="Main Menu",
                             clear_screen=True)
    choice = main_menu.show()
    if choice == 0:
        show_movies_menu()
    elif choice == 1:
        show_lists_menu()
    elif choice == 2:
        pass
    elif choice == 3:
        exit()

def main():
    """
    Main function for starting things up.
    """
    # show_options()
    # TODO: implement login functionality
    show_main_menu()

if __name__ == "__main__":
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    # conn = get_conn()
    main()
