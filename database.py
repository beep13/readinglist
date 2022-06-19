# title, release_date, watched

CREATE_BOOKS_TABLE = """CREATE TABLE IF NOT EXISTS books(
    title TEXT,
    release_timestamp REAL,
    watched INTEGER
);"""

INSERT_BOOKS = "INSERT INTO books (titles, release_timestamp, watched) VALUES (?, ?, 0);"
SELECT_ALL_BOOKS = "SELECT * FROM books;"
SELECT_UPCOMING_BOOKS = "SELECT * FROM books WHERE release_timestamp > ?;"
SELECT_READ_BOOKS = "SELECT * FROM movies WHERE watched = 1;"
