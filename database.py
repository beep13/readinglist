import datetime
import sqlite3
from urllib.parse import ParseResultBytes

CREATE_BOOKS_TABLE = """CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY,
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

INSERT_BOOKS = "INSERT INTO books (title, release_timestamp) VALUES (?, ?);"
INSERT_USER = "INSERT INTO users (username) VALUES (?);"
DELETE_MOVIE = "DELETE FROM books WHERE  title = ?;"
SELECT_ALL_BOOKS = "SELECT * FROM books;"
SELECT_UPCOMING_BOOKS = "SELECT * FROM books WHERE release_timestamp > ?;"
SELECT_READ_BOOKS = """SELECT * FROM books
JOIN read on books.id = read.book_id
JOIN users on users.username = read.user_username
WHERE users.username = ?;"""
INSERT_READ_BOOK = "INSERT INTO read (user_username, book_id) VALUES (?, ?);"
SET_BOOK_WATCHED = "UPDATE books SET read = 1 WHERE title = ?;"


connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_BOOKS_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_READ_TABLE)


def add_user(username):
    with connection:
        connection.execute(INSERT_USER, (username,))


def add_book(title, release_timestamp):
    with connection:
        connection.execute(INSERT_BOOKS, (title, release_timestamp))


def get_books(upcoming=False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_BOOKS, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_BOOKS)
        return cursor.fetchall()


def read_book(username, book_id):
    with connection:
        connection.execute(INSERT_READ_BOOK, (username, book_id))


def get_read_books(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_READ_BOOKS, (username,))
        return cursor.fetchall()
