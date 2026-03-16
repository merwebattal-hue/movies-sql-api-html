import sqlite3

DB_NAME = "movies.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year TEXT,
        rating TEXT,
        poster TEXT
    )
    """)

    conn.commit()
    conn.close()


def get_movies():
    conn = get_connection()
    movies = conn.execute("SELECT * FROM movies ORDER BY id DESC").fetchall()
    conn.close()
    return movies


def add_movie(title, year, rating, poster):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO movies (title, year, rating, poster)
    VALUES (?, ?, ?, ?)
    """, (title, year, rating, poster))

    conn.commit()
    conn.close()


def delete_movie(movie_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))

    conn.commit()
    conn.close()


def update_movie(movie_id, new_title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE movies
    SET title = ?
    WHERE id = ?
    """, (new_title, movie_id))

    conn.commit()
    conn.close()


def movie_exists(title):
    conn = get_connection()
    movie = conn.execute(
        "SELECT * FROM movies WHERE title = ?",
        (title,)
    ).fetchone()
    conn.close()
    return movie