import unittest
from archive.data.csv_file_handler import CsvFileHandler
from machine_learning.content_based.content_based import ContentBased


class TestContentBased(unittest.TestCase):

    def setUp(self):
        self.movies = CsvFileHandler("../archive/data", "sample_movie_dataset.csv")
        self.movies.extract_data()
        self.movies_data_frame = self.movies.get_data_frame()

        self.valid_cb = ContentBased("Avatar", self.movies_data_frame, ["Title", "Genre", "Director", "Actors"])
        self.invalid_cb = ContentBased("Avatar", self.movies_data_frame, ["Title", "Ge", "Director", "Actors"])

    def test_constructor(self):
        self.assertIsInstance(self.valid_cb, ContentBased)
        self.assertIsInstance(self.invalid_cb, ContentBased)
        self.assertRaises(TypeError, ContentBased, "Avatar", None, None)
        self.assertRaises(TypeError, ContentBased, None, self.movies_data_frame, None)
        self.assertRaises(TypeError, ContentBased, None, None, [])
        self.assertRaises(TypeError, ContentBased, None, None, None)

    def test_filter(self):
        self.assertIsInstance(self.valid_cb.filter(), list)
        self.assertRaises(KeyError, self.invalid_cb.filter)


if __name__ == '__main__':
    unittest.main()
