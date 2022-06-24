import os
import datetime
import psycopg2

from dotenv import load_dotenv

load_dotenv()

CREATE_BOOKS_TABLE = """CREATE TABLE IF NOT EXISTS books(
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);"""

CREATE_READ_TABLE = """CREATE TABLE IF NOT EXISTS read (
    user_username TEXT,
    book_id INTEGER, 
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(book_id) REFERENCES books(id)
);"""

INSERT_BOOKS = "INSERT INTO books (title, release_timestamp) VALUES (%s, %s);"
INSERT_USER = "INSERT INTO users (username) VALUES (%s);"
DELETE_MOVIE = "DELETE FROM books WHERE  title = %s;"
SELECT_ALL_BOOKS = "SELECT * FROM books;"
SELECT_UPCOMING_BOOKS = "SELECT * FROM books WHERE release_timestamp > %s;"
SELECT_READ_BOOKS = """SELECT * FROM books
JOIN read on books.id = read.book_id
JOIN users on users.username = read.user_username
WHERE users.username = %s;"""
INSERT_READ_BOOK = "INSERT INTO read (user_username, book_id) VALUES (%s, %s);"
SET_BOOK_WATCHED = "UPDATE books SET read = 1 WHERE title = %s;"
SEARCH_BOOKS = "SELECT * FROM books WHERE title LIKE %s;"
CREATE_PUBLISH_INDEX = "CREATE INDEX IF NOT EXISTS idx_books_release ON books(release_timestamp);"

connection = psycopg2.connect(os.environ["DATABASE_URL"])


def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_BOOKS_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_READ_TABLE)
            cursor.execute(CREATE_PUBLISH_INDEX)


def add_user(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))


def add_book(title, release_timestamp):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_BOOKS, (title, release_timestamp))


def get_books(upcoming=False):
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_BOOKS, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_BOOKS)
            return cursor.fetchall()


def search_books(search_term):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_BOOKS, (f"%{search_term}%",))
            return cursor.fetchall()


def read_book(username, book_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_READ_BOOK, (username, book_id))


def get_read_books(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_READ_BOOKS, (username,))
            return cursor.fetchall()
