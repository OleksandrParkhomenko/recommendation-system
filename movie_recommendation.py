import numpy as np
import pandas as pd


class MovieRecommendation:

    def __init__(self, ):
        self.__read_data()
        self.__preprocess_data()

    def __read_data(self):
        r_cols = ['userId', 'movieId', 'rating']
        self.ratings = pd.read_csv('data/movies/ratings.csv', usecols=r_cols, header=0, )
        m_cols = ['movieId', 'title', 'genres']
        self.movies = pd.read_csv('data/movies/movies.csv', usecols=m_cols, header=0, index_col='movieId')

    def __preprocess_data(self):
        self.__extract_year()
        self.__separate_genres()
        print(self.movies.head(10))
        # print(self.movies[['year', 'title']])

    def __extract_year(self):
        self.movies['year'] = self.movies['title'].str.extract('(\(\d\d\d\d\))', expand=False)
        self.movies['year'] = self.movies['year'].str.extract('(\d\d\d\d)', expand=False)
        # delete year from title
        self.movies['title'] = self.movies['title'].str.replace('(\(\d\d\d\d\))', "")
        self.movies['title'] = self.movies['title'].apply(lambda x: x.strip())

    def __separate_genres(self):
        self.movies['genres'] = self.movies['genres'].str.split("|")
        self.genre_table = self.movies.copy()
        for index, row in self.movies.iterrows():
            for genre in row['genres']:
                self.genre_table.at[index, genre] = 1
        self.genre_table = self.genre_table.fillna(0)
        self.genre_table = self.genre_table.drop(columns=['(no genres listed)', 'genres', 'year', 'title'])
        print(self.genre_table)

    def get_content_based_recommendation(self, user_preferences, amount=10):
        pass

    def get_emotion_based_recommendation(self, emotion):
        pass


if __name__ == "__main__":
    userInput = [
        {'title': 'Breakfast Club, The', 'rating': 5},
        {'title': 'Toy Story', 'rating': 3.5},
        {'title': 'Jumanji', 'rating': 2},
        {'title': "Pulp Fiction", 'rating': 5},
        {'title': 'Akira', 'rating': 4.5}
    ]
    inputMovies = pd.DataFrame(userInput)

    test = MovieRecommendation()
    movie_title = "Terminator, The (1984)"
    import datetime

    start = datetime.datetime.now()
    # similar = test.get_similar_movies(movie_title)
    time_spent = datetime.datetime.now() - start
    # print(similar)
    print("It takes: ", time_spent)
