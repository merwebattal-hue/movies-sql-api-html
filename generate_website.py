import movie_storage_sql as storage


def generate_website():
    """Generate a static HTML website from the movie database."""
    movies = storage.list_movies()

    html_start = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Movie App</title>
        <style>
            body {
                background-color: #f4f4f4;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
            }

            h1 {
                text-align: center;
            }

            .movie-grid {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
            }

            .movie-card {
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                width: 220px;
                padding: 15px;
                text-align: center;
            }

            .movie-card img {
                width: 100%;
                height: auto;
                border-radius: 8px;
            }

            .movie-title {
                font-size: 18px;
                font-weight: bold;
                margin-top: 10px;
            }

            .movie-year,
            .movie-rating {
                margin: 5px 0;
            }
        </style>
    </head>
    <body>
        <h1>My Movie Collection 🎬</h1>
        <div class="movie-grid">
    """

    html_end = """
        </div>
    </body>
    </html>
    """

    movie_cards = ""

    for title, data in movies.items():
        poster = data.get("poster", "")
        year = data.get("year", "N/A")
        rating = data.get("rating", "N/A")

        movie_cards += f"""
        <div class="movie-card">
            <img src="{poster}" alt="{title} poster">
            <div class="movie-title">{title}</div>
            <div class="movie-year">Year: {year}</div>
            <div class="movie-rating">Rating: {rating}</div>
        </div>
        """

    full_html = html_start + movie_cards + html_end

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(full_html)

    print("Website was generated successfully.")


if __name__ == "__main__":
    generate_website()