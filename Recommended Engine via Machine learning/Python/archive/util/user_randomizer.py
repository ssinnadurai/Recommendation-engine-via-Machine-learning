from random import randint, random
from pandas import DataFrame, concat, Series
from pprint import pprint


class UserRandomization:

    def __init__(self, movie_database, count=10000):
        self.data_frame = movie_database
        self.count = count
        self.profile = DataFrame({
            "Users": [],
            "Movie": [],
            "Rating": []
        })

    def create_user(self):
        user_list = []
        for i in range(self.count):
            user_list.append(i+1)

        for user in user_list:
            self.__randomizer(user)

        return self.profile

    def __randomizer(self, user):
        for i in range(0, 5):
            # choose a random movie from the database
            random_int = randint(0, len(self.data_frame) - 1)
            chosen_movie = self.data_frame.iloc[random_int]
            self.profile = self.profile.append(
                {"Users": user, "Movie": chosen_movie["Title"], "Rating": str(2 + random() * 8)[:3]}, ignore_index=True)

    # Creating Temporary User Profile. Will be replace with database's user profile
    def temp_create_user_profile(movie_pd):
        user_set = UserRandomization(movie_pd)
        user_database = user_set.create_user()
        print(user_database)
        writer = 'C:\\Users\\sharu\\PycharmProjects\\Sharusshan\\Collaborative User Data 3.csv'
        user_database.to_csv(writer, index=True)