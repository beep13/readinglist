import datetime
import sqlite3
from urllib.parse import ParseResultBytes

CREATE_BOOKS_TABLE = """CREATE TABLE IF NOT EXISTS books(
    title TEXT,
    release_timestamp REAL
);"""

CREATE_READLIST_TABLE = """CREATE TABLE IF NOT EXISTS read (
    reader_name TEXT,
    title TEXT
);"""

INSERT_BOOKS = "INSERT INTO books (title, release_timestamp) VALUES (?, ?);"
DELETE_MOVIE = "DELETE FROM books WHERE  title = ?;"
SELECT_ALL_BOOKS = "SELECT * FROM books;"
SELECT_UPCOMING_BOOKS = "SELECT * FROM books WHERE release_timestamp > ?;"
SELECT_READ_BOOKS = "SELECT * FROM read WHERE reader_name = ?;"
INSERT_READ_BOOK = "INSERT INTO read (reader_name, title) VALUES (?, ?)"
SET_BOOK_WATCHED = "UPDATE books SET read = 1 WHERE title = ?;"


connection = sqlite3.connect("data.db")

def create_tables():
    with connection:
        connection.execute(CREATE_BOOKS_TABLE)
        connection.execute(CREATE_READLIST_TABLE)


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


def read_book(username, title):
    with connection:
        connection.execute(DELETE_MOVIE, (title, ))
        connection.execute(INSERT_READ_BOOK, (username, title))


def get_read_books(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_READ_BOOKS, (username,))
        return cursor.fetchall()
