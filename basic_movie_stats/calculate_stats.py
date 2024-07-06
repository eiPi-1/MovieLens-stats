import os
import json
import pandas as pd
from collections import Counter
import logging
from typing import Union
logger = logging.getLogger(__name__)


class MovieLensStats:

    def __init__(self, dataset_path='../MovieLens/', path_relative=True):
        """
        Creates an object of a class that computes statistics and analytics on the MovieLens dataset.
        :param dataset_rel_path: The relative path (w.r.t. module location) of the MovieLens dataset.
        """
        if path_relative:
            class_dir = os.path.dirname(__file__)
            abs_path = os.path.join(class_dir, dataset_path)
        else:
            abs_path = dataset_path
        self.metadata_df = pd.read_csv(os.path.join(abs_path, 'movies_metadata.csv'))
        self.ratings_df = pd.read_csv(os.path.join(abs_path, 'ratings.csv'))
        self.links_df = pd.read_csv(os.path.join(abs_path, 'links.csv'))

        self._clear_duplicates_metatada()
        self._clean_imdbid_metadata()
        self._eval_to_strict_metadata()
        self._convert_genres_to_list()

    def _clear_duplicates_metatada(self, on_column: str = 'imdb_id'):
        """
        Making sure there are no duplicate records.

        :param on_column: the name of the column against which to check and disregard duplications
        """
        try:
            self.metadata_df.dropna(subset=['imdb_id'], inplace=True)
            self.metadata_df.drop_duplicates(subset=[on_column], inplace=True)
        except KeyError:
            logger.error(f"Column with name {on_column} does not exist in the dataframe.")

    def _clean_imdbid_metadata(self):
        """
        In metadata imdb_id are stored in the format of tt followed by 7 digits, i.e. tt0114709
        but in other files such as ratings.csv, imdb ids are stored just as integers (without leading 0s).
        That is why here we remove the leading tt and 0s and also drop any rows with NaN imdb ids.
        """
        self.metadata_df['imdb_id'] = self.metadata_df['imdb_id'].str.replace('tt', '').astype(int)
        tmp = pd.to_datetime(self.metadata_df['release_date'], format='%Y-%m-%d', errors='coerce')
        # if format did not match return Nan, source: https://stackoverflow.com/questions/64455709/drop-rows-where-column-value-not-valid-date-pandas
        self.metadata_df = self.metadata_df[tmp.notna()]

    def _eval_to_strict_metadata(self, on_column: str = 'genres'):
        """
        Evaluates values a particular column in metadata df from string into data structure.
        Particularly for the 'genres' column, the genres to which a movie belongs are represented as a
        list of dictionaries, however this list of dictionaries is stored in the column as a string that
        represents a pythonic list of dictionaries.
        :param on_column: the column name that is to be evaluated
        """
        try:
            self.metadata_df[on_column] = self.metadata_df[on_column].apply(eval)
        except KeyError:
            logger.error(f"Column with name {on_column} does not exist in the dataframe.")

    def get_num_unique_movies(self) -> int:
        """
        Returns the number of unique movies in the dataset

        :return: number of unique movies
        """
        return self.metadata_df.imdb_id.nunique()

    def get_avg_rating_all(self) -> float:
        return self.ratings_df['rating'].mean()

    def get_top_rated_movies(self, top_n: int = 5) -> Union[list, None]:
        """
        Returns the n top rated movies.

        :param top_n: specifies how many of the top rated movies to return
        :return: List of the titles of the top n rated movies or None.
        """
        if top_n >= self.ratings_df.shape[0]:
            logger.error("Value for argument top_n is larger than the number of rows in the dataframe.")
            return

        top_ratings_movieIds = self.ratings_df.sort_values(by='rating', ascending=False).iloc[0:top_n].movieId.tolist()
        top_ratings_imdbIds = self.links_df[self.links_df['movieId'].isin(top_ratings_movieIds)].imdbId.tolist()

        return self.metadata_df[self.metadata_df['imdb_id'].isin(top_ratings_imdbIds)].title.to_list()

    def get_num_movies_per_year(self) -> dict:
        """
        Returns the number of movies released each year.

        :return: Dataframe of number movies per year.
        """
        self.metadata_df['release_year'] = pd.DatetimeIndex(self.metadata_df['release_date']).year
        movies_per_year_df = self.metadata_df['release_year'].value_counts().rename_axis('release_year').reset_index(name='number_movies')
        movies_per_year_df['release_year'] = movies_per_year_df['release_year'].astype(int)

        res = pd.Series(
            movies_per_year_df['number_movies'].values,
            index=movies_per_year_df['release_year']
        ).sort_index(ascending=False).to_dict()

        return res

    def get_num_movies_per_genre(self) -> dict:
        """
        Returns the number of movies released each genre.

        :return: Dictionary of number movies per year.
        """

        genres_list = sum(self.metadata_df['genres'].to_list(), [])
        genre_frequency = dict(Counter(genres_list))

        return genre_frequency

    def _convert_genres_to_list(self):
        self.metadata_df['genres'] = self.metadata_df['genres'].apply(lambda x: [el["name"] for el in x])


def main():
    movie_stats = MovieLensStats()

    n_unique_movies = movie_stats.get_num_unique_movies()
    avg_rating_all_movies = round(movie_stats.get_avg_rating_all(), 2)
    top_rated_movies = movie_stats.get_top_rated_movies()
    year_to_num_movies = movie_stats.get_num_movies_per_year()
    genre_to_num_movies = movie_stats.get_num_movies_per_genre()

    print("")
    print(f"Number of unique movies: {n_unique_movies}")
    print(f"Average rating for all movies: {avg_rating_all_movies}")
    print(f"Top 5 rated movies: {top_rated_movies}")
    print(f"Number of movies released each year:")
    print(pd.DataFrame(year_to_num_movies.items(), columns=['year', 'number of movies']))
    print("Number of movies in each genre:")
    print(pd.DataFrame(genre_to_num_movies.items(), columns=['genre', 'number of movies']))

    stats = {"Number of unique movies": n_unique_movies,
             "Average rating for all movies": avg_rating_all_movies,
             "Top 5 rated movies": top_rated_movies,
             "Number of movies released each year (year: num. movies)": year_to_num_movies,
             "Number of movies in each genre": genre_to_num_movies
             }

    with open("../results.json", "w") as outfile:
        outfile.write(json.dumps(stats, indent=4))


if __name__ == "__main__":
    main()
