# Use
The project implements a class used to analyse and provide statistics for the MovieLens dataset.

# Reunning it
To run the file from within basic-movie-stats:
```
python basic_movie_stats/calculate_stats.py
```

Note:
For purposes of keeping the package small, the MovieLens dataset is not included. It can be downloaded from https://www.kaggle.com/rounakbanik/the-movies-dataset
Example file structure with which this project was developed and tests:


```
├── basic-movie-stats
│   ├── basic_movie_stats
│   │   ├── calculate_stats.py
│   ├── MovieLens
│	│	├── creduts.csv
│	│	├── ...
│	│	├── ratings_small.csv
│	├── tests
│   │		├── test_calculate_stats.py
├── poetry.lock
├── poetry.toml
├── README.md
└── .gitignore
```

# Testing
For local testing run:
```
python -m unittest
```

Note: The unit tests can be expanded in order to test the helper functions for cleaning and filtering out invalid data etc.