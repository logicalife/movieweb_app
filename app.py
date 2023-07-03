from flask import Flask, jsonify, render_template, redirect, url_for, request
from datamanager.json_data_manager import JSONDataManager
import json
import requests

app = Flask(__name__)
data_manager = JSONDataManager('storage/movies.json')
MOVIE_API_URL = "http://www.omdbapi.com/?apikey=67fde472&"


@app.route('/', methods=['GET'])
def home():
    """This function defines the home page of the web application"""
    return render_template("home.html"), 200


@app.route('/users')
def list_users():
    """This function returns rendered HTML page to display User's list for this route"""
    users_list = data_manager.get_all_users()
    return render_template("users.html", users=users_list), 200  # Returns a rendered HTML for list of users with link


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """This function accepts user_id as parameter and returns rendered HTML page for the list of movies for that user"""
    user_list = data_manager.get_all_users()
    if user_id not in [user[1] for user in user_list]:
        return jsonify('User not found!')
    movie_list = data_manager.get_user_movies(user_id)
    return render_template('movie_list.html', movies=movie_list, user_id=user_id), 200
    # This will exhibit a specific user’s list of movies


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """This function returns new_user_form on GET request
    and returns list of users after creating new user on POST request"""
    if request.method == 'GET':
        return render_template('new_user_form.html'), 200
        # This will present a form that enables the addition of a new user
    if request.method == 'POST':
        user_list = data_manager.get_all_users()
        # list of all users in tuple (username,User_id)
        new_username = request.form.get('name')
        new_userid = max([int(user[1]) for user in user_list]) + 1
        if new_username in [user[0] for user in user_list]:
            return jsonify("Username already exists!")
        data_manager.add_user(new_username, new_userid)
        return redirect(url_for('list_users')), 201


@app.route('/users/<int:user_id>/add_movie', methods=["GET", "POST"])
def add_movie(user_id):
    """This function accepts user_id as parameter returns new_movie_form on GET request
    and returns list of movies for that users after creating new movie on POST request"""
    if request.method == 'GET':
        return render_template('new_movie_form.html', user_id=user_id), 200
        # This will present a form that enables the addition of a new user
    if request.method == 'POST':
        movies_list = data_manager.get_user_movies(user_id)
        user_list = data_manager.get_all_users()  # list of all users in tuple (username,User_id)
        if user_id not in [int(user[1]) for user in user_list]:  # checking if user_id is valid
            return jsonify(f"User with userid -{user_id} doesn't exists!"), 204
        try:       # assigning new unique user_id
            new_movie_id = max([int(movie['id']) for movie in movies_list]) + 1
        except ValueError:
            new_movie_id = 1
        movie_data = json.loads(requests.get(MOVIE_API_URL + "t=" + request.form.get('name')).text)
        # getting movie data from OMDB URL
        if "Error" in movie_data:
            return jsonify(f'{movie_data["Error"]}')
        new_movie = {"id": int(new_movie_id), "name": movie_data["Title"], 'year': movie_data["Year"],
                     'rating': movie_data["Ratings"][0]["Value"].split("/")[0],
                     'director': movie_data['Director'],
                     'poster_link': movie_data['Poster']
                     }
        data_manager.add_movie(user_id, new_movie)
        return redirect(url_for('user_movies', user_id=str(user_id))), 201


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['GET'])
def delete_movie(user_id, movie_id):
    """This function accepts user_id and movie_id as parameter,
    and deletes the movie from user's Movie list."""
    user_list = data_manager.get_all_users()
    if user_id not in [user[1] for user in user_list]:
        # Checking if user_id is valid
        return jsonify('User not found!'), 200
    movie_list = data_manager.get_user_movies(user_id)
    for movie in movie_list:  # Checking if movie with movie_id is available.
        if movie['id'] == movie_id:
            data_manager.delete_movie(user_id, movie_id)
            return redirect(url_for('user_movies', user_id=user_id))
    return jsonify("Movie_id is not valid")


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """This route will display a form allowing for the updating of details 
    of a specific movie in a user’s list."""
    user_list = data_manager.get_all_users()
    movie_list = data_manager.get_user_movies(user_id)
    if user_id not in [user[1] for user in user_list]:  # Checking if user_id is valid
        return jsonify('User not found!')
    if movie_id not in [movie['id'] for movie in movie_list]:  # Checking if movie with movie_id is available.
        return jsonify("Movie_id is not valid")
    for movie in movie_list:
        if movie['id'] == movie_id:
            movie_to_update = movie
            break
    if request.method == "GET":
        return render_template('update.html', user_id=user_id, movie_id=movie_id, movie=movie_to_update)
    if request.method == "POST":
        new_movie_name = request.form.get('name')
        new_movie_director = request.form.get('director')
        new_movie_year = request.form.get('year')
        new_movie_rating = request.form.get('rating')
        data_manager.update_movie(user_id, movie_id, new_movie_name, new_movie_director,
                                  new_movie_year, new_movie_rating)
        return redirect(url_for('user_movies', user_id=user_id))


if __name__ == "__main__":
    app.run(debug=True)
