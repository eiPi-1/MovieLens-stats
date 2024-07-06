import os
import unittest
import pandas as pd
from basic_movie_stats.calculate_stats import MovieLensStats


class TestMovieLensStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Running setUpClass')
        metadata_df = pd.DataFrame({'imdb_id': ['tt01', 'tt02', 'tt03', 'tt04', 'tt05', 'tt06', 'tt05'],
                                    'genres': ["[{'id': 16, 'name': 'Animation'}, {'id': 35, 'name': 'Comedy'}, {'id': 10751, 'name': 'Family'}]",
                                               "[{'id': 12, 'name': 'Adventure'}, {'id': 14, 'name': 'Fantasy'}, {'id': 10751, 'name': 'Family'}]",
                                               "[{'id': 10749, 'name': 'Romance'}, {'id': 35, 'name': 'Comedy'}]",
                                               "[{'id': 35, 'name': 'Comedy'}, {'id': 18, 'name': 'Drama'}, {'id': 10749, 'name': 'Romance'}]",
                                               "[{'id': 35, 'name': 'Comedy'}]", "[{'id': 10749, 'name': 'Romance'}, {'id': 35, 'name': 'Comedy'}]",
                                               "[{'id': 35, 'name': 'Comedy'}]"],
                                    'vote_average': [7.7, 6.9, 6.5, 6.1, 5.7, 5.2, 5.7],
                                    'release_date': ['1995-10-30', '1995-12-15', '1995-12-22', '1995-12-22', '1995-02-10', '1999-03-13', '1995-02-10'],
                                    'title': ["Movie 1", "Movie 2", "Movie 3", "Movie 4", "Movie 5", "Movie 6", "Movie 5"]})

        ratings_df = pd.DataFrame({'userId': [270896, 270896, 1, 270896, 270896, 270896],
                                   'movieId': [21, 22, 23, 24, 25, 26],
                                   'rating': [10, 8.9, 9.1, 2.3, 5.5, 7.6]})

        links_df = pd.DataFrame({'imdbId': [1, 2, 3, 4, 5, 6],
                                 'movieId': [21, 22, 23, 24, 25, 26],
                                 'rating': [10, 8.9, 9.1, 2.3, 5.5, 7.6]})

        metadata_df.to_csv('movies_metadata.csv')
        ratings_df.to_csv('ratings.csv')
        links_df.to_csv('links.csv')

        cls.movies_stats = MovieLensStats(dataset_path='.', path_relative=False)

    @classmethod
    def tearDownClass(cls):
        print('Running tearDownClass')
        os.remove('movies_metadata.csv')
        os.remove('ratings.csv')
        os.remove('links.csv')

    def test_clear_metadata(self):
        assert self.movies_stats.metadata_df.shape[0] == 6
        assert self.movies_stats.metadata_df['imdb_id'].to_list() == [1, 2, 3, 4, 5, 6]

    def test_num_unique_movies(self):
        assert self.movies_stats.get_num_unique_movies() == 6

    def test_avg_rating(self):
        assert round(self.movies_stats.get_avg_rating_all(), 2) == 7.23

    def test_top_rated_movies(self):
        assert self.movies_stats.get_top_rated_movies(2) == ["Movie 1", "Movie 3"]

    def test_movies_per_year(self):
        assert self.movies_stats.get_num_movies_per_year() == {1995: 5, 1999: 1}

    def test_movies_per_genre(self):
        expected_res = {'Animation': 1, 'Comedy': 5, 'Family': 2,
                        'Adventure': 1, 'Fantasy': 1, 'Romance': 3, 'Drama': 1}
        assert self.movies_stats.get_num_movies_per_genre() == expected_res


if __name__ == '__main__':
    unittest.main()
