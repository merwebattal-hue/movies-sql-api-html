import random
import movie_storage_sql as storage
from api_fetch import fetch_movie
from generate_website import generate_website


def select_user():
    """Benutzer auswählen. Standardmäßig wird 'Merve' zurückgegeben."""
    return {"id": 1, "name": "Merve"}


def command_list_movies(user):
    """Alle Filme in der Datenbank auflisten."""
    movies = storage.list_movies()
    if not movies:
        print("\nDeine Filmsammlung ist aktuell leer.")
        return

    print(f"\n--- {user['name']}s Filmsammlung ({len(movies)} Filme) ---")
    for title, data in movies.items():
        note_str = f" | Notiz: {data['note']}" if data['note'] else ""
        print(f"🎬 {title} ({data['year']}) - Bewertung: ⭐ {data['rating']}{note_str}")


def command_add_movie(user):
    """Einen neuen Film über die OMDb API hinzufügen."""
    title = input("Geben Sie den Namen des Films ein: ").strip()
    if not title:
        print("Fehler: Der Filmname darf nicht leer sein.")
        return

    print(f"Suche nach '{title}'...")
    movie_data = fetch_movie(title)

    if movie_data:

        user_note = input(f"Persönliche Notiz für '{movie_data['title']}' (optional): ").strip()


        storage.add_movie(
            movie_data["title"],
            movie_data["year"],
            movie_data["rating"],
            movie_data["poster"],
            user_note,
            movie_data["imdbID"],
            movie_data["country"],

        )
    else:
        print("Film konnte nicht hinzugefügt werden. Bitte überprüfen Sie den Titel.")


def command_delete_movie(user):
    """Einen film aus der Datenbank löschen."""
    title = input("Name des zu löschenden Films: ").strip()
    if title:
        storage.delete_movie(title)
    else:
        print("Der Name darf nicht leer sein.")


def command_update_movie(user):
    """Die Bewertung eines Films aktualisieren."""
    title = input("Name des Films für das Update: ").strip()
    try:
        new_rating = float(input(f"Neue Bewertung für '{title}' (0-10): "))
        if 0 <= new_rating <= 10:
            storage.update_movie(title, new_rating)
        else:
            print("Die Bewertung muss zwischen 0 und 10 liegen.")
    except ValueError:
        print("Ungültige Eingabe. Bitte geben Sie eine Zahl ein.")


def command_movie_stats(user):
    """Statistiken über die Filmsammlung anzeigen."""
    movies = storage.list_movies()
    if not movies:
        print("Keine Filme für Statistiken vorhanden.")
        return

    ratings = [data["rating"] for data in movies.values()]
    avg_rating = sum(ratings) / len(ratings)
    max_rating = max(ratings)
    best_movies = [title for title, data in movies.items() if data["rating"] == max_rating]

    print("\n--- Statistiken ---")
    print(f"📊 Durchschnittliche Bewertung: {avg_rating:.2f}")
    print(f"🏆 Beste Bewertung: {max_rating}")
    print(f"🌟 Top Film(e): {', '.join(best_movies)}")


def command_random_movie(user):
    movies = storage.list_movies()
    if not movies:
        print("Keine Filme vorhanden.")
        return
    title = random.choice(list(movies.keys()))
    print(f"Zufälliger Film-Tipp: {title} ({movies[title]['year']})")


def print_menu():
    """Das Hauptmenü anzeigen."""
    print("\n" + "=" * 25)
    print(" FILMDATENBANK MENÜ ")
    print("=" * 25)
    print("1. Filme auflisten")
    print("2. Film hinzufügen")
    print("3. Film löschen")
    print("4. Bewertung aktualisieren")
    print("5. Statistiken")
    print("6. Zufälliger Film")
    print("9. Website generieren")
    print("0. Beenden")


def main():
    active_user = select_user()
    print(f"\nWillkommen bei der Film-App, {active_user['name']}!")

    while True:
        print_menu()
        choice = input("\nIhre Wahl (0-9): ").strip()

        if choice == "0":
            print("Auf Wiedersehen! Viel Spaß beim Filmeschauen! 🍿")
            break
        elif choice == "1":
            command_list_movies(active_user)
        elif choice == "2":
            command_add_movie(active_user)
        elif choice == "3":
            command_delete_movie(active_user)
        elif choice == "4":
            command_update_movie(active_user)
        elif choice == "5":
            command_movie_stats(active_user)
        elif choice == "6":
            command_random_movie(active_user)
        elif choice == "9":
            generate_website(active_user)
        else:
            print("Ungültige Wahl. Bitte versuchen Sie es erneut.")


if __name__ == "__main__":
    main()