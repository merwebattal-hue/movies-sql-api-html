from sqlalchemy import create_engine, text

DB_URL = "sqlite:///movies_sqlalchemy_v2.db"
engine = create_engine(DB_URL, echo=False)

def init_db():
    """Initialisiert die Datenbank mit der Tabelle 'movies'."""
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster TEXT,
                note TEXT,
                imdb_id TEXT,
                country TEXT  -- YENİ: Ülke bilgisi için sütun eklendi
            )
        """))
        connection.commit()

init_db()

def list_movies():
    """Gibt alle Filme als Dictionary zurück."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster, note, imdb_id, country FROM movies"))
        movies = result.fetchall()

    return {
        row[0]: {
            "year": row[1],
            "rating": row[2],
            "poster": row[3],
            "note": row[4] if row[4] is not None else "",
            "imdb_id": row[5] if row[5] is not None else "",
            "country": row[6] if row[6] is not None else "" # YENİ: Ülke bilgisi
        }
        for row in movies
    }

def add_movie(title, year, rating, poster, note="", imdb_id="", country=""): # Parametre eklendi
    """Fügt einen neuen Film mit Notiz, IMDb ID und Land zur Datenbank hinzu."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("""
                    INSERT INTO movies (title, year, rating, poster, note, imdb_id, country)
                    VALUES (:title, :year, :rating, :poster, :note, :imdb_id, :country)
                """),
                {
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "poster": poster,
                    "note": note,
                    "imdb_id": imdb_id,
                    "country": country # YENİ
                }
            )
            connection.commit()
            print(f"Film '{title}' wurde erfolgreich hinzugefügt.")
        except Exception as e:
            print(f"Fehler beim Hinzufügen: {e}")

def delete_movie(title):
    with engine.connect() as connection:
        result = connection.execute(text("DELETE FROM movies WHERE title = :t"), {"t": title})
        connection.commit()
        if result.rowcount > 0:
            print(f"Film '{title}' wurde gelöscht.")
        else:
            print(f"Film '{title}' nicht gefunden.")

def update_movie(title, rating):
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :r WHERE title = :t"),
            {"r": rating, "t": title}
        )
        connection.commit()
        if result.rowcount > 0:
            print(f"Bewertung für '{title}' aktualisiert.")
        else:
            print(f"Film '{title}' nicht gefunden.")