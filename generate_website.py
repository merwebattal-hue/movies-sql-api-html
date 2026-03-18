import movie_storage_sql as storage
import os

COUNTRY_FLAGS = {
    "USA": "🇺🇸",
    "United States": "🇺🇸",
    "UK": "🇬🇧",
    "United Kingdom": "🇬🇧",
    "Turkey": "🇹🇷",
    "Türkiye": "🇹🇷",
    "France": "🇫🇷",
    "Germany": "🇩🇪",
    "Italy": "🇮🇹",
    "Japan": "🇯🇵",
    "South Korea": "🇰🇷",
    "Canada": "🇨🇦",
    "Spain": "🇪🇸"
}


def get_flag(country_string):
    if not country_string:
        return "🌐"
    first_country = country_string.split(",")[0].strip()
    return COUNTRY_FLAGS.get(first_country, "🌐")


def generate_website(user):
    """Erstellt eine HTML-Datei basierend auf den Filmen in der Datenbank."""
    movies = storage.list_movies()

    # Üst kısım: Başlık ve Rastgele Film Seçici Butonu
    html_content = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <title>{user['name']}s Filmbibliothek</title>
        <link rel="stylesheet" href="static/style.css">
    </head>
    <body>
        <div class="list-movie-title">
            <h1>🎬 {user['name']}s Filmbibliothek</h1>
            <button onclick="pickRandomMovie()" class="random-btn">🎲 Zufälliger Film</button>
        </div>
        <div>
            <ul class="movie-grid"> 
    """

    for title, data in movies.items():
        imdb_id = data.get('imdb_id', '')
        imdb_url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "#"
        flag = get_flag(data.get('country', ''))

        movie_html = f"""
            <li>
                <div class="movie">
                    <a href="{imdb_url}" target="_blank">
                        <img class="movie-poster" src="{data['poster']}" title="{data['note']}">
                    </a>
                    <div class="movie-title">{title} {flag}</div>
                    <div class="movie-year">{data['year']}</div>
                    <div class="movie-rating">⭐ {data['rating']}</div>
                </div>
            </li>
        """
        html_content += movie_html

    # Alt kısım: JavaScript Sihri (Rastgele filmi seçer, odaklanır ve parlatır)
    html_content += """
            </ul>
        </div>

        <script>
        function pickRandomMovie() {
            // Tüm film kartlarını bul
            const movies = document.querySelectorAll('.movie');
            if (movies.length === 0) {
                alert("Zuerst musst du einige Filme hinzufügen!");
                return;
            }

            // Varsa önceki seçimin efektini temizle
            movies.forEach(m => {
                m.style.border = "none";
                m.style.boxShadow = "none";
            });

            // Rastgele bir index seç
            const randomIndex = Math.floor(Math.random() * movies.length);
            const selected = movies[randomIndex];

            // Seçilen filme yumuşak bir geçiş yap
            selected.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // Seçilen filmi vurgula (Netflix kırmızısı çerçeve ve parlama)
            selected.style.border = "4px solid #e50914";
            selected.style.boxShadow = "0 0 20px #e50914";
            selected.style.borderRadius = "8px";
            selected.style.transition = "all 0.5s ease";

            // Küçük bir kutlama mesajı
            const movieTitle = selected.querySelector('.movie-title').innerText;
            setTimeout(() => {
                alert("🎬 Heute schauen wir: " + movieTitle);
            }, 600);
        }
        </script>
    </body>
    </html>
    """

    file_name = f"{user['name']}.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Website erfolgreich generiert: {file_name}")