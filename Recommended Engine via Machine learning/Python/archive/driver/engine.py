import pandas as pd
from archive.data.csv_file_handler import CsvFileHandler
from machine_learning.content_based.content_based import ContentBased
from machine_learning.collaborative_based.collaborative_filtering import CollaborativeBased
from pprint import pprint

# display to console setting
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def get_datagram(path, file):
    data_object = CsvFileHandler(path, file)
    data_object.extract_data()
    return data_object.get_data_frame()


# Content Based filtering based on selected category
def content_based_filtering(key, movies, filter_list=["Title", "Genre", "Director", "Actors"]):
    cb = ContentBased(key, movies, filter_list)
    return cb.filter()


# Collaborative Based filtering based on selected items liked by other users
def collaborative_based_filtering(user_profiles, uid):
    cb = CollaborativeBased(user_profiles, uid)
    if cb.generate_recommended_results():
        return cb.get_recommended_results()
    return False


def get_recommendation_collaborative_based(selected_key=3):
    path_user_profiles = "../data"
    file_user_profiles = "user_profile_logs.csv"
    user_profile_movie_data = get_datagram(path_user_profiles, file_user_profiles)
    result = collaborative_based_filtering(user_profile_movie_data, selected_key)
    return result


def get_recommendation_content_based(movie_title):
    path_movies_csv = "../data"
    file_movies_csv = "sample_movie_dataset.csv"
    movie_csv = get_datagram(path_movies_csv, file_movies_csv)
    result = content_based_filtering(movie_title, movie_csv, )
    return result[:10]


# Program main
if __name__ == "__main__":
    path_movies_csv = "../data"
    file_movies_csv = "sample_movie_dataset.csv"
    path_user_profiles = "../data"
    file_user_profiles = "user_profile_logs.csv"

    selected_key = "American Honey"
    user_id = 1

    movie_csv = get_datagram(path_movies_csv, file_movies_csv)
    user_profile_movie_data = get_datagram(path_user_profiles, file_user_profiles)

    #result = collaborative_based_filtering(user_profile_movie_data, user_id)

    #if isinstance(result, bool) and not result:
    result = content_based_filtering(selected_key, movie_csv, )

    pprint(result)
