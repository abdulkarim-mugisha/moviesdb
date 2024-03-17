# CS 121 Final Project: Movies Database Application

This is an interactive command-line interface (CLI) application designed to browse, review, and manage movies and movie lists. This application allows users to explore movies by various criteria, manage personalized movie lists, and contribute reviews. The database is implemented using MySQL, and the application is developed using Python.

## Features

- **Browse Movies**: Discover movies by popularity, genre, rating, or year.
- **Movie Details**: View detailed information about movies, including descriptions, runtime, director, cast, and average ratings.
- **Review Movies**: Contribute reviews and ratings for movies.
- **Manage Movie Lists**: Create personalized movie lists, add movies to lists, and view all available lists.
- **User Accounts**: Support for both regular users and admin users with additional privileges, such as adding or deleting movies.

## Getting Started

Steps to set up and run the Movie Review Application.

1. Clone the repository and cd to the repository directory.
2. Run the following mySQL commands in this order to set up the database and set the necessary permissions:

    ```txt
    CREATE DATABASE moviesdb;
    USE moviesdb;
    SET GLOBAL local_infile=1;
    source setup.sql;
    source load-data.sql;
    source setup-passwords.sql;
    source setup-routines.sql;
    source grant-permissions.sql;
    source queries.sql;
    ```

3. Install the python dependencies using `pip install -r requirements.txt`.
4. Start the application by running `python3 app.py` from your command line.

## Usage

#### Navigation

Use the arrow keys to navigate through menu options and press Enter to select menu items.

#### User Type Selection

Upon starting the application, you will first be asked to select your user type: Client or Admin. This choice determines the subsequent authentication process.

#### Authentication Process

- **Admin Login**: Admin users are required to log in using their username and password.
- **Client Login or Account Creation**:
    - Existing clients can log in by entering their username and password.
    - New clients can select the option to create an account, following the prompts to enter their desired username, password, and bio.

You can use the following credentials to login:
- *Client Account* 
  - Username: `vwells`
  - Password: `vwellspw`
- *Admin Account* 
  - Username: `ebennett`
  - Password: `ebennettpw`


#### Client Functionality

After logging in or creating an account as a client, you will be greeted with the main menu:

- **Browse Movies**: Explore the movie database.
- **Browse Movie Lists**: View and manage custom movie lists.
- **Log out / Quit**: Sign out of the application or quit the program.

Click through the menu options to explore the application's client features.

#### Admin Functionality

After logging in as an admin, you will have access to these options:

- **Add New Movies**: Add new movies to the database.
- **Delete Movies**: Remove existing movies from the database.
- **Manage Users**: Delete user accounts.
- **Manage Lists**: Delete movie lists.
- **Log Out / Quit**: Sign out of the application or quit the program.

Click through the menu options to explore the application's admin features.


## Dataset
The CSV data in the folder `data` was extracted from the Kaggle dataset [TMDB Movies](https://www.kaggle.com/datasets/alanvourch/tmdb-movies-daily-updates).

## Unfinished Features 

- Follower functionality. Subscribing to other users to view lists of the users
you follow. 
- Adding new admins. 
- Pagination for navigation through large movie results lists.
- Breadcrumbs (more sophisticated functionality for going back in menus).
