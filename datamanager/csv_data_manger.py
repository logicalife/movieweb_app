from data_manager_interface import DataManagerInterface


class CSVDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return a list of all users
        pass

    def get_user_movies(self, user_id):
        # Return a list of all movies in dictionary
        pass

    def add_user(self, username, userid):
        pass

    def add_movie(self, userid, new_movie):
        pass

    def delete_movie(self, user_id, movie_id):
        pass

    def update_movie(self, user_id, movie_id):
        pass
