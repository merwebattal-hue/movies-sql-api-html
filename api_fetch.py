import requests

API_KEY = "172fa515"


def fetch_movie(title):
    """Ruft Filmdaten von der OMDb API ab."""
    clean_title = title.strip()
    url = f"https://www.omdbapi.com/?apikey={API_KEY}&t={clean_title}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("Response") != "True":
            print(f"Fehler: Film '{clean_title}' wurde nicht gefunden.")
            return None

        # Jahr bereinigen
        year_raw = data.get("Year", "0")
        year = int(year_raw[:4]) if year_raw[:4].isdigit() else 0

        # Bewertung bereinigen
        rating_raw = data.get("imdbRating", "0")
        rating = float(rating_raw) if rating_raw != "N/A" else 0.0

        return {
            "title": data.get("Title"),
            "year": year,
            "rating": rating,
            "poster": data.get("Poster"),
            "imdbID": data.get("imdbID"),
            "country": data.get("Country"),
            "note": ""
        }
    except Exception as e:
        print(f"API-Fehler: {e}")
        return None