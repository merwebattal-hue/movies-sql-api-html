import requests

API_KEY = "172fa515"


def fetch_movie(title):
    """Fetch movie data from OMDb API."""
    url = f"https://www.omdbapi.com/?apikey={API_KEY}&t={title}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        print("Error: OMDb API is not accessible.")
        return None

    if data.get("Response") != "True":
        print("Error: Movie not found.")
        return None

    rating = data.get("imdbRating")
    if rating == "N/A":
        rating = 0.0
    else:
        rating = float(rating)

    return {
        "title": data.get("Title"),
        "year": int(data.get("Year")),
        "rating": rating,
        "poster": data.get("Poster")
    }