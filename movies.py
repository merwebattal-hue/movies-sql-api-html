import random
import movie_storage_sql as storage
from api_fetch import fetch_movie
from generate_website import generate_website

def command_list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()
    print(f"\n{len(movies)} movies in total\n")

    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")
        print(f"Poster: {data['poster']}")
        print()


def command_add_movie():
    """Prompt the user for a movie title and add it using the OMDb API."""
    title = input("Enter new movie name: ")

    movie = fetch_movie(title)

    if movie:
        storage.add_movie(
            movie["title"],
            movie["year"],
            movie["rating"],
            movie["poster"]
        )


def command_delete_movie():
    """Prompt the user for a movie title and delete it from the database."""
    title = input("Enter movie name to delete: ")
    storage.delete_movie(title)


def command_update_movie():
    """Prompt the user for a movie title and new rating, then update the movie."""
    title = input("Enter movie name to update: ")
    rating = float(input("Enter new movie rating: "))

    storage.update_movie(title, rating)


def command_movie_stats():
    """Calculate and display statistics about the movies."""
    movies = storage.list_movies()

    if not movies:
        print("No movies in database.")
        return

    ratings = [data["rating"] for data in movies.values()]
    avg_rating = sum(ratings) / len(ratings)
    max_rating = max(ratings)
    min_rating = min(ratings)

    best_movies = [movie for movie, data in movies.items() if data["rating"] == max_rating]
    worst_movies = [movie for movie, data in movies.items() if data["rating"] == min_rating]

    print(f"Average rating: {avg_rating:.2f}")
    print(f"Highest rating: {max_rating}")
    print("Best movie(s): " + ", ".join(best_movies))
    print(f"Lowest rating: {min_rating}")
    print("Worst movie(s): " + ", ".join(worst_movies))


def command_random_movie():
    """Select and display a random movie from the database."""
    movies = storage.list_movies()

    if not movies:
        print("No movies in database.")
        return

    movie = random.choice(list(movies.keys()))
    data = movies[movie]
    print(f"Your random movie is: {movie} ({data['year']}), rating: {data['rating']}")


def print_menu():
    """Display the main menu."""
    print("\nMenu:")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("9. Generate website")


def main():
    """Run the movie application menu loop."""
    while True:
        print_menu()
        choice = input("Enter choice (0-6): ")

        if choice == "0":
            print("Bye!")
            break
        elif choice == "1":
            command_list_movies()
        elif choice == "2":
            command_add_movie()
        elif choice == "3":
            command_delete_movie()
        elif choice == "4":
            command_update_movie()
        elif choice == "5":
            command_movie_stats()
        elif choice == "6":
            command_random_movie()
        elif choice == "9":
            generate_website()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()