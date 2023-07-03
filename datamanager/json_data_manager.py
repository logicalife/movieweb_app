import json
from datamanager.data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, location):
        self.filename = location

    def get_all_users(self):
        """This function accepts no argument and returns a list of Users from JSON data file"""
        with open(self.filename, "r") as fileobj:
            data = json.loads(fileobj.read())
        user_list = []
        for user in data:
            user_list.append((user["name"], user["id"]))
        return user_list   # Returns a list of tuples (usernames,user_id)

    def get_user_movies(self, user_id):
        """This function accepts User_id as parameter and returns a list of movies
        in dictionary formate for that user"""
        with open(self.filename, "r") as fileobj:
            data = json.loads(fileobj.read())
        for user in data:
            if int(user["id"]) == user_id:
                return user["movies"]  # Returns a list of dictionaries

    def add_user(self, username, userid):
        """This function accepts Username as the parameter and returns a list of updated user list"""
        with open(self.filename, "r") as fileobj:
            data = json.loads(fileobj.read())
        data.append({"id": userid, "name": username, "movies": []})
        with open(self.filename, "w") as fileobj:  # Writing file with updated data.
            fileobj.write(json.dumps(data))

    def add_movie(self, user_id, new_movie):
        with open(self.filename, "r") as fileobj:  # Opening and reading storage file
            data = json.loads(fileobj.read())
        for user in data:  # Looking for the correct movie and deleting.
            if int(user["id"]) == user_id:
                user['movies'].append(new_movie)
        with open(self.filename, "w") as fileobj:  # Writing file with updated data.
            fileobj.write(json.dumps(data))

    def delete_movie(self, user_id, movie_id):
        """This function accepts user_id and movie_id as parameter,
            and deletes the movie from user's Movie list."""
        with open(self.filename, "r") as fileobj:  # Opening and reading storage file
            data = json.loads(fileobj.read())
        for user in data:  # Looking for the correct movie and deleting.
            if int(user["id"]) == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        user['movies'].remove(movie)
        with open(self.filename, "w") as fileobj:  # Writing file with updated data.
            fileobj.write(json.dumps(data))

    def update_movie(self, user_id, movie_id, new_name, new_director, new_year, new_rating):
        with open(self.filename, "r") as fileobj:  # Opening and reading storage file
            data = json.loads(fileobj.read())
        for user in data:  # Looking for the correct movie and updating when found.
            if int(user["id"]) == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        movie['name'] = new_name
                        movie['director'] = new_director
                        movie['year'] = new_year
                        movie['rating'] = new_rating
        with open(self.filename, "w") as fileobj:  # Writing file with updated data.
            fileobj.write(json.dumps(data))
