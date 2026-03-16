from flask import Flask, render_template, request, redirect
from database import create_table, get_movies, add_movie, delete_movie, movie_exists
from api_fetch import fetch_movie

app = Flask(__name__)

create_table()

@app.route("/")
def home():
    movies = get_movies()
    return render_template("index.html", movies=movies)

@app.route("/add", methods=["POST"])
def add_movie_route():
    title = request.form["title"]

    if movie_exists(title):
        return redirect("/")

    movie = fetch_movie(title)

    if movie:
        add_movie(movie["title"], movie["year"], movie["rating"], movie["poster"])

    return redirect("/")

@app.route("/delete/<int:movie_id>")
def delete_movie_route(movie_id):
    delete_movie(movie_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)