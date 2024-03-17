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
import textwrap

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
def get_conn(is_admin=True):
    """
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin1" if is_admin else "client1",
            # Find port in MAMP or MySQL Workbench GUI or with
            # SHOW VARIABLES WHERE variable_name LIKE 'port';
            port="3306",  # this may change!
            password="admin1pw" if is_admin else "client1pw",
            database="moviesdb",  # replace this with your database name
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
    CALL calc_movie_rating({movie_id});
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
    return rows[0][1]


def view_movies_by_popularity():
    """
    Provides a list of the most popular movies.
    """
    global BACK_FUNCTION
    BACK_FUNCTION = view_movies_by_popularity
    cursor = conn.cursor()
    sql = """
    SELECT m.movie_id, m.title, EXTRACT(YEAR FROM m.release_date), COUNT(r.movie_id) as review_count
    FROM movie m
    LEFT JOIN review r ON m.movie_id = r.movie_id
    GROUP BY m.movie_id
    ORDER BY review_count DESC
    LIMIT 10;
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
        movies = [f"{row[1]} ({row[2]})" for row in rows]
        ids = [row[0] for row in rows]
        display_movies(movies, ids)


def view_movies_by_genre():
    """
    Provides a list of all the movies of a given genre.
    """
    global BACK_FUNCTION
    BACK_FUNCTION = view_movies_by_genre
    genre = input("Enter the genre: ")
    cursor = conn.cursor()
    sql = f"""
    SELECT m.movie_id, m.title, EXTRACT(YEAR FROM m.release_date)
    FROM movie m
    JOIN movie_genre mg ON m.movie_id = mg.movie_id
    WHERE mg.genre = '{genre}'
    LIMIT 10;
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
        movies = [f"{row[1]} ({row[2]})" for row in rows]
        ids = [row[0] for row in rows]
        display_movies(movies, ids)


def view_movies_by_year():
    """
    Provides a list of all the movies released in a given year
    """
    global BACK_FUNCTION
    BACK_FUNCTION = view_movies_by_year
    year = input("Please enter the release year: ")
    cursor = conn.cursor()
    sql = (
        "SELECT movie_id, title, EXTRACT(YEAR FROM release_date) FROM movie WHERE YEAR(release_date) = '%s' ORDER BY title ASC LIMIT 10;"
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
        movies = [f"{row[1]} ({row[2]})" for row in rows]
        ids = [row[0] for row in rows]
        display_movies(movies, ids)


def view_movies_by_rating():
    """
    Provides a list of the movies ordered by rating.
    """
    global BACK_FUNCTION
    BACK_FUNCTION = view_movies_by_rating
    cursor = conn.cursor()
    sql = """
    SELECT m.movie_id, m.title, AVG(r.rating) as average_rating
    FROM movie m
    LEFT JOIN review r ON m.movie_id = r.movie_id
    GROUP BY m.movie_id
    ORDER BY average_rating DESC, m.title ASC LIMIT 10;  
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
        movies = [f"{row[1]} (average rating: {row[2]:.1f})" for row in rows]
        ids = [row[0] for row in rows]
        display_movies(movies, ids)


def write_a_review():
    """
    Writes a review for a movie. Prompts the user for their user ID, the movie ID,
    their rating, and their review text, then inserts this information into the reviews table.
    """
    rating = input("Please rate the movie (0.0 to 5.0): ")
    new_review = input("Write your review: ")
    sql = """
    CALL add_or_update_review(%s, %s, %s, %s);
    """ % (
        CURRENT_USER_ID,
        CURRENT_MOVIE_ID,
        rating,
        new_review
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


def create_list(title, description):
    """
    Creates a list of movies.
    """
    cursor = conn.cursor()
    sql = """
    INSERT INTO list (created_by, title, description)
    VALUES (%s, %s, %s);
    """ % (
        CURRENT_USER_ID,
        title,
        description,
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


def add_movie_to_list(list_id):
    """
    Adds a movie to a user's list by inserting a record into the list_movies table.
    """
    cursor = conn.cursor()
    sql = f"""
    CALL add_movie_to_list({list_id}, {CURRENT_MOVIE_ID});
    """
    try:
        existing_movie_query = f"""
        SELECT 1 FROM movie_in_list 
        WHERE list_id = {list_id} AND movie_id = {CURRENT_MOVIE_ID};
        """
        if cursor.execute(existing_movie_query).fetchone():
            print("This movie is already in the list.")
        else:
            cursor.execute(sql)
            conn.commit()
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
    sql = f"""
    CALL remove_movie_from_list({list_id}, {movie_id});
    """
    try:
        cursor.execute(sql)
        conn.commit()
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
    """
    Searches for movies by name. Returns a list of movies that match the query.
    """
    cursor = conn.cursor()
    sql = """
    SELECT movie_id, title, YEAR(release_date) FROM movie WHERE title LIKE '%s';
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
    """
    Searches for movies by id. Returns a list of movies that match the query.
    """
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
    """
    Returns all the movies in a given list_id.
    """
    cursor = conn.cursor()
    sql = """
    SELECT m.movie_id, m.title, YEAR(release_date) FROM movie m
    JOIN movie_in_list mil ON m.movie_id = mil.movie_id
    WHERE mil.list_id = %s;
    """ % (
        list_id
    )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        # list_of_movie_dicts = []
        # for row in rows:
        #     list_of_movie_dicts.append({"movie_id": row[0]})
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when getting movies in list.")
            return
    # return list_of_movie_dicts
    return rows

def add_movie(movie):
    """ "
    Adds a movie to the database.
    Args:
        movie: A dictionary representing a movie with the keys "title", 
               "release_date", "description", "director", "cast", "runtime".
    """
    cursor = conn.cursor()
    sql = """
    INSERT INTO movie (title, release_date, description, director, cast, runtime)
    VALUES (%s, %s, %s, %s, %s, %s);
    """ % (
        movie["title"],
        movie["release_date"],
        movie["description"],
        movie["director"],
        movie["cast"],
        movie["runtime"],
    )
    try:
        cursor.execute(sql)
        print("Your new movie has been successfully added.")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when adding a movie.")
            return


def delete_user(user_id):
    """ "
    Deletes a user from the database.
    Args:
        user_id: The id of the user to delete.
    """
    cursor = conn.cursor()
    sql = """
    DELETE FROM user_account WHERE user_id = %s;
    """ % (
        user_id
    )
    try:
        cursor.execute(sql)
        if cursor.rowcount > 0:
            print("The user has been successfully deleted.")
        else:
            print("The user was not found in the database.")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when deleting the user.")
            return


def delete_list(list_id):
    """
    Deletes a list from the database given the list id.
    Args:
        list_: The id of the user to delete.
    """
    cursor = conn.cursor()
    sql = """
    DELETE FROM list WHERE list_id = %s;
    """ % (
        list_id
    )
    try:
        cursor.execute(sql)
        if cursor.rowcount > 0:
            print("The list has been successfully deleted.")
        else:
            print("The list was not found in the database.")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when deleting the list.")
            return


def delete_movie(movie_id):
    """
    Deletes a movie from the database given the movie id.
    Args:
        movie_id: The id of the movie to delete.
    """
    cursor = conn.cursor()
    sql = """
    DELETE FROM movie WHERE movie_id = %s;
    """ % (
        movie_id
    )
    try:
        cursor.execute(sql)
        if cursor.rowcount > 0:
            print("The movie has been successfully deleted.")
        else:
            print("The movie was not found in the database.")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when deleting the movie.")
            return
        
def get_list_details(list_id):
    """
    Returns the a dictionary representing the details of the list with the 
    given list_id.
    """
    cursor = conn.cursor()
    sql = "SELECT * FROM list WHERE list_id LIKE %s;" % (list_id)
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when getting the title of the list.")
            return
    details_dict = {
        "list_id": rows[0][0],
        "created_by": rows[0][1],
        "title": rows[0][2],
        "description": rows[0][3],
        "date_created": rows[0][4],
    }
    return details_dict


def get_movie_details(movie_id):
    """
    Returns a dictionary representing the details of the movie with the 
    given movie_id.
    """
    cursor = conn.cursor()
    sql = "SELECT * FROM movie WHERE movie_id LIKE %s;" % (movie_id)
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when getting the title of the list.")
            return
    details_dict = {
        "movie_id": rows[0][0],
        "title": rows[0][1],
        "release_date": rows[0][2],
        "description": rows[0][3],
        "director": rows[0][4],
        "cast": rows[0][5],
        "runtime": rows[0][6],
    }
    return details_dict

def get_movie_reviews(movie_id):
    """
    Returns all reviews for a given movie.
    """
    cursor = conn.cursor()
    sql =  f"""
    SELECT get_reviews_for_movie({movie_id});
    """ 
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        reviews = []
        for row in rows:
            reviews.append(f"{row[0]}\t({row[1]})\t{row[2]}")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when getting the title of the list.")
            return
    return reviews

# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)
def authenticate_user(username, password):
    """
    Authenticates a user given a username and password, and updates
    the CURRENT_USER_ID global variable.
    """
    global CURRENT_USER_ID
    conn = get_conn()
    cursor = conn.cursor()
    sql = f"""
    CALL authenticate('{username}', '{password}');
    """
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("Invalid username or password.")
            return False
        else:
            CURRENT_USER_ID = rows[0][0]
            return True
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred in authenticating the user.")


def create_user():
    """
    Creates a new user by prompting for a username, password, and bio.
    """
    username = input("Choose a username: ")
    password = input("Enter a password: ")
    bio = input("Enter a short bio, press Enter to skip: ")
    sql = f"""
    CALL sp_add_user('{username}', '{password}', '{bio}', 0);
    """
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except mysql.connector.Error as err:  # okay let me see
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred in creating the user.")
    authenticate_user(username, password)


def show_account_options():
    """
    Displays the menu for user type selection.
    """
    user_options = ["Admin", "Client", "Quit"]
    user_menu = TerminalMenu(
        user_options, title="Select your user type", clear_screen=True
    )
    print("Welcome to the Movie Database!")
    choice = user_menu.show()
    if choice == 0:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if authenticate_user(username, password):
            show_admin_menu()
    elif choice == 1:
        options = ["Login", "Create an account", "Quit"]
        start_menu = TerminalMenu(options)
        choice = start_menu.show()
        if choice == 0:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if authenticate_user(username, password):
                show_client_main_menu()
        elif choice == 1:
            create_user()
            show_client_main_menu()
        elif choice == 2:
            exit()

    elif choice == 2:
        exit()


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------


def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print("Good bye!")
    exit()


def display_movies(movies, ids):
    """ 
    Displays a menu of movies as results, allowing the user to select a movie to
    view details.

    """
    movies.append("Go Back")
    results_menu = TerminalMenu(movies, title=f"{len(movies) - 1} results:")
    choice = results_menu.show()
    if choice == 10:
        show_movies_menu()
    else: 
        show_movie_details(ids[choice])

def show_list(list_id):
    """
    Displays the details of a specific movie list, including all movies 
    in the list.

    """
    rows = get_movies_in_list(list_id)
    movies = [f"{row[1]} ({row[2]})" for row in rows]
    ids  = [f"{row[0]}" for row in rows]
    list_details = get_list_details(list_id)
    list_menu = TerminalMenu(movies, title=f"List: {list_details['title']}")
    choice = list_menu.show()
    show_movie_details(ids[choice], list_id=list_id)


def display_lists(lists, ids, on_click_fn=show_list):
    """ 
    Displays a menu of lists, allowing the user to select a list to view its 
    details or perform an action.

    """
    lists.append("Go Back")

    results_menu = TerminalMenu(lists, title=f"{len(lists)} results:")
    choice = results_menu.show()
    if choice == len(lists) - 1:
        BACK_FUNCTION()
    else: 
        on_click_fn(ids[choice])


def show_movie_search_menu():
    """
    Displays a search menu that prompts the user to enter a movie title for 
    search and displays the results.

    """
    query = input("Enter movie title: ")
    rows = search_movies_by_name(query)
    movies = [f"{row[1]} ({row[2]})" for row in rows]
    ids = [f"{row[0]}" for row in rows]
    display_movies(movies, ids)


def show_movies_menu():
    """
    Displays the main movies menu with various options to browse and search 
    movies.
    """
    global BACK_FUNCTION
    BACK_FUNCTION = show_movies_menu
    options = [
        "View movies by popularity",
        "View movies by genre",
        "View movies by rating",
        "View movies by year",
        "Search for a Movie",
        "Go back",
    ]
    movies_menu = TerminalMenu(options, title="Movies")
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
        show_client_main_menu()


def show_lists_menu():
    """
    Displays the lists menu, offering options to view, create, or manage 
    movie lists.

    """
    global BACK_FUNCTION
    BACK_FUNCTION = show_lists_menu
    options = ["My Lists", "All lists", "Create List", "Go back"]
    lists_menu = TerminalMenu(options, title="Lists")
    choice = lists_menu.show()
    if choice == 0:
        rows = show_my_lists()
        lists = [f"{row[1]}" for row in rows]
        ids = [row[0] for row in rows]
        display_lists(lists, ids)
    elif choice == 1:
        rows = show_all_lists()
        lists = [f"{row[1]}" for row in rows]
        ids = [row[0] for row in rows]
        display_lists(lists, ids)
    elif choice == 2:
        title = input("Please enter the title of your new list: ")
        description = input("Please enter a description for your new list: ")
        create_list(title, description)
    elif choice == 3:
        show_client_main_menu()


def show_my_lists():
    """ "
    Returns all lists created by the current user.
    """
    cursor = conn.cursor()
    sql = """
    SELECT list_id, title, description, date_created FROM list
    WHERE created_by = %s;
    """ % (
        CURRENT_USER_ID
    )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when getting user's lists.")
            return
    return rows


def show_all_lists():
    """
    Returns  all lists in the database.
    """
    cursor = conn.cursor()
    sql = "SELECT list_id, title, description, date_created FROM list;"
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("An error occurred when getting all lists.")
            return
    return rows
        

def show_movie_details(movie_id, list_id=None):
    global CURRENT_MOVIE_ID
    CURRENT_MOVIE_ID = movie_id
    options = ["Review Movie"]
    if list_id:
        options.append("Remove from List")
    else:
        options.append("Save to List")
    options.append("Go Back")
    movie_details = get_movie_details(movie_id)
    movie_rating = find_movie_rating(movie_id)
    title = f"""
    {movie_details['title']} ({movie_details['release_date'].year})
    {textwrap.fill(movie_details['description'], width=80, subsequent_indent="    ")}
    
    {movie_details['runtime']//60}h {movie_details['runtime']%60}min
    Rating: {movie_rating}
    
    Directed by {movie_details['director']}
    Starring {textwrap.fill(movie_details['cast'], width=80, subsequent_indent="    ")}
    
    Reviews:
    {"\n".join(get_movie_reviews(movie_id))}
    """
    movie_details_menu = TerminalMenu(options, title=title, clear_screen=True)
    choice = movie_details_menu.show()
    if choice == 0:
        write_a_review()
    elif choice == 1:
        if list_id:
            remove_movie_from_list(list_id, CURRENT_MOVIE_ID)
        else: 
            rows = show_my_lists()
            lists = [f"{row[1]}" for row in rows]
            ids = [row[0] for row in rows]
            display_lists(lists, ids, on_click_fn=add_movie_to_list)
    elif choice == 2:
        if list_id:
            show_list(list_id)
        else:
            BACK_FUNCTION()


def show_client_main_menu():
    options = ["Browse Movies", "Browse Movie Lists", "Log out", "Quit"]
    main_menu = TerminalMenu(options, title="Main Menu", clear_screen=True)
    choice = main_menu.show()
    if choice == 0:
        show_movies_menu()
    elif choice == 1:
        show_lists_menu()
    elif choice == 2:
        global CURRENT_USER_ID
        CURRENT_USER_ID = None
        show_account_options()
    elif choice == 3:
        exit()


def show_admin_menu():
    options = ["Add Movie", "Delete Movie", "Delete User", "Delete List", "Log Out", "Quit"]
    admin_menu = TerminalMenu(options, title="Choose an option")
    choice = admin_menu.show()
    if choice == 0:
        # query admin to add movie
        movie = {}
        movie["title"] = input("Enter the movie title: ")
        movie["release_date"] = input("Enter the release data: ")
        movie["description"] = input("Enter the description: ")
        movie["director"] = input("Enter the director(s): ")
        movie["cast"] = input("Enter the cast: ")
        movie["runtime"] = input("Enter the runtime in minutes: ")
        add_movie(movie)
    elif choice == 1:
        movie_id = input("Enter the movie ID: ")
        delete_movie(movie_id)
    elif choice == 2:
        user_id = input("Enter the user ID: ")
        delete_user(user_id)
    elif choice == 3:
        list_id = input("Enter the list ID: ")
        delete_list(list_id)
    elif choice == 4:
        global CURRENT_USER_ID
        CURRENT_USER_ID = None
        show_account_options()
    elif choice == 5:
        exit()
    
def main():
    """
    Main function for starting things up.
    """
    show_account_options()


if __name__ == "__main__":
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    CURRENT_USER_ID = None
    CURRENT_MOVIE_ID = None
    BACK_FUNCTION = show_client_main_menu
    conn = get_conn()
    main()

