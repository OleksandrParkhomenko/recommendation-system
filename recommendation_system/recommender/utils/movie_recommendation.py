import numpy as np
import pandas as pd
from textblob import TextBlob


class MovieRecommendation:

    def __init__(self, ):
        self.__read_data()
        self.__preprocess_data()

    def __read_data(self):
        r_cols = ['userId', 'movieId', 'rating']
        self.ratings = pd.read_csv('../../../data/movies/ratings.csv', usecols=r_cols, header=0)
        m_cols = ['movieId', 'title', 'genres']
        self.movies = pd.read_csv('../../../data/movies/movies.csv', usecols=m_cols, header=0)
        l_cols = ['movieId', 'imdbId']

    def __preprocess_data(self):
        self.__extract_year()
        self.__separate_genres()

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

    def __preprocess_user_data(self, user_preferences):
        user_preferences = pd.DataFrame(user_preferences)
        movies_id = self.movies[self.movies['title'].isin(user_preferences['title'].tolist())]
        user_preferences = movies_id.merge(user_preferences, left_on='title', right_on='title')
        user_preferences = user_preferences.drop(columns=['genres', 'year'])
        return user_preferences

    def __get_user_genre_table(self, user_preferences):
        user_genre_table = self.genre_table[self.genre_table['movieId'].isin(user_preferences['movieId'].tolist())]
        user_genre_table = user_genre_table.reset_index(drop=True)
        user_genre_table = user_genre_table.drop(columns=['movieId'])
        user_profile = user_genre_table.transpose().dot(user_preferences['rating'])
        return user_profile

    def get_content_based_recommendation(self, user_preferences, amount=20):
        user_preferences = self.__preprocess_user_data(user_preferences)
        user_preferences = self.__get_user_genre_table(user_preferences)
        genre_table = self.genre_table.set_index([self.genre_table['movieId']])
        genre_table = genre_table.drop(columns=['movieId'])
        recommendation_table = ((genre_table * user_preferences).sum(axis=1)) / user_preferences.sum()
        recommendation_table = recommendation_table.sort_values(ascending=False)
        if amount == -1:
            return self.movies.loc[self.movies['movieId'].isin(recommendation_table.keys())]
        return self.movies.loc[self.movies['movieId'].isin(recommendation_table.head(amount).keys())]

    def __get_emotion(self, text):
        polarity = TextBlob(text).sentiment.polarity
        scaled_polarity = ((((polarity + 1) * 100) // 1) - 1) // 50
        return scaled_polarity

        # total_deviation

    # example -0.38 0.62 62
    # negative
    # -1 0 0
    # -0.5 0.5 5
    # 0 1 10
    # 0.5 1.5 15
    # 1 2 20
    # positive

    def get_emotion_based_recommendation(self, total_deviation, user_preferences, amount=20):
        movies = self.get_content_based_recommendation(user_preferences, -1)
        movies['emotion_difference'] = movies.apply(
            lambda row: abs(self.__get_emotion(row['title']) - total_deviation), axis=1)
        return movies.sort_values(by=['emotion_difference'], ascending=[False]).head(amount)


if __name__ == "__main__":
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', 180)
    test_user_input = [

        {'title': 'Breakfast Club, The', 'rating': 5},
        {'title': 'Toy Story', 'rating': 3.5},
        {'title': 'Jumanji', 'rating': 2},
        {'title': "Pulp Fiction", 'rating': 5},
        {'title': 'Akira', 'rating': 4.5}

    ]
    test = MovieRecommendation()

    import datetime

    start = datetime.datetime.now()
    # movies = test.get_content_based_recommendation(test_user_input)
    movies = test.get_emotion_based_recommendation(2, test_user_input)
    print(movies)
    time_spent = datetime.datetime.now() - start
    print("It takes: ", time_spent)
