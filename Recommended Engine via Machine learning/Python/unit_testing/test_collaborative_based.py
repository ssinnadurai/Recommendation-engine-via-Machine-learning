from content_based import ContentBased
import unittest
from pymongo import MongoClient
from pandas import DataFrame


class testContentBased(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['moviesDB']
        self.collection = self.db['movies']
        self.test_df = DataFrame(list(self.collection.find()))

        self.valid_cb = ContentBased("_id", "5f96e0b8639a72229e0fd042", self.test_df,
                                     ["Title", "Genre", "Director", "Actors"])
        self.recs = self.valid_cb.get_recommendations(10, "Rating")

    def test_constructor(self):
        self.assertIsInstance(self.valid_cb, ContentBased)
        self.assertRaises(TypeError, ContentBased, "_id", None, None, None)
        self.assertRaises(TypeError, ContentBased, None, "5f96e0b8639a72229e0fd042", None, None)
        self.assertRaises(TypeError, ContentBased, None, self.test_df, None, None)
        self.assertRaises(TypeError, ContentBased, None, None, None, [])
        self.assertRaises(TypeError, ContentBased, None, None, None, None)
        # Since the consructor call the sort_frame() function these tests serve to test that as well
        self.assertRaises(KeyError, ContentBased, "_id", "5f96e0b8639a72229e0fd042", self.test_df,
                          ["Title", "Ge", "Director", "Actors"])
        self.assertRaises(Exception, ContentBased, "_id", "blah123", self.test_df,
                          ["Title", "Genre", "Director", "Actors"])

    def test_get_recommendations(self):
        self.assertIsInstance(self.recs, list)
        self.assertIsInstance(self.recs[0], dict)
        self.assertRaises(KeyError, self.valid_cb.get_recommendations, 10, "Bad Value")


if __name__ == '__main__':
    unittest.main()

























import unittest
from archive.data.csv_file_handler import CsvFileHandler
from machine_learning.collaborative_based.collaborative_filtering import CollaborativeBased


class TestCollaborativeBased(unittest.TestCase):

    def setUp(self):
        self.user_profiles = CsvFileHandler("../archive/data", "user_profile_logs.csv")
        self.user_profiles.extract_data()
        self.user_profiles_data_frame = self.user_profiles.get_data_frame()

        self.valid_cb = CollaborativeBased(self.user_profiles_data_frame, 3)
        self.valid_cb.generate_recommended_results()
        self.invalid_cb = CollaborativeBased(self.user_profiles_data_frame, -1)
        self.invalid_cb.generate_recommended_results()

    def test_constructor(self):
        self.assertIsInstance(self.valid_cb, CollaborativeBased)
        self.assertIsInstance(self.invalid_cb, CollaborativeBased)
        self.assertRaises(TypeError, CollaborativeBased, self.user_profiles_data_frame, "")
        self.assertRaises(TypeError, CollaborativeBased, self.user_profiles_data_frame, 3.14)
        self.assertRaises(TypeError, CollaborativeBased, self.user_profiles_data_frame, None)
        self.assertRaises(TypeError, CollaborativeBased, [], 1)
        self.assertRaises(TypeError, CollaborativeBased, None, 2)

    def test_filter(self):
        self.assertTrue(self.valid_cb.generate_recommended_results())
        self.assertFalse(self.invalid_cb.generate_recommended_results())

    def test_get_recommended_results(self):
        self.assertIsInstance(self.valid_cb.get_recommended_results(), list)
        self.assertEquals(self.invalid_cb.get_recommended_results(), [])


if __name__ == '__main__':
    unittest.main()
