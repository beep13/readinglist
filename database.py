import datetime
import sqlite3
from urllib.parse import ParseResultBytes

CREATE_BOOKS_TABLE = """CREATE TABLE IF NOT EXISTS books(
    title TEXT,
    release_timestamp REAL,
    watched INTEGER
);"""

INSERT_BOOKS = "INSERT INTO books (titles, release_timestamp, watched) VALUES (?, ?, 0);"
SELECT_ALL_BOOKS = "SELECT * FROM books;"
SELECT_UPCOMING_BOOKS = "SELECT * FROM books WHERE release_timestamp > ?;"
SELECT_READ_BOOKS = "SELECT * FROM movies WHERE watched = 1;"

connection = sqlite3.connect("data.db")

def create_tables():
    with connection:
        connection.execute(CREATE_BOOKS_TABLE)


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


def read_book(title):
    pass

def get_read_books():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_READ_BOOKS)
        return cursor.fetchall()