import pandas as pd


class MusicRecommendation:

    def __init__(self):
        cols = ['loudness', 'tempo', 'key', 'artist.name', 'artist.id', 'title', 'year', 'song.id',
                'artist.hotttnesss', 'song.hotttnesss', 'artist_mbtags', 'terms']
        self.music = pd.read_csv('../../../data/music/music.csv', header=0, usecols=cols)
        self.music.rename(columns={'artist.hotttnesss': 'artist.popularity',
                                   'song.hotttnesss': 'popularity',
                                   'artist_mbtags': 'artist.tags',
                                   'terms': 'tags'},
                          inplace=True)
        self.__normalize_music_data()
        self.__merge_tags()
        print(self.music[['tags']].sample(10))

    def __merge_tags(self):
        self.music['artist.tags'] = self.music['artist.tags'].fillna("")
        self.music['tags'] = self.music['tags'].fillna("")
        self.music['tags.test'] = self.music['tags'] + " " + self.music['artist.tags']
        self.music.drop(columns=['artist.tags'])

    def __normalize_music_data(self):
        self.__normalize_column('key')
        self.__normalize_column('tempo')
        self.__normalize_column('loudness')

    def __normalize_column(self, column_name):
        self.music[column_name] = ((((self.music[column_name] - self.music[column_name].min()) / (
                self.music[column_name].max() - self.music[column_name].min())) * 100) - 1) // 20

    def get_songs_for_mood(self, mood, amount=10):
        song_mood_corr = pd.read_csv('../../../data/music/music_mood_classification.csv', index_col=0, header=0)
        loudness = song_mood_corr.loc[mood]['loudness']
        key = song_mood_corr.loc[mood]['key']
        tempo = song_mood_corr.loc[mood]['tempo']
        self.music['difference'] = self.music.apply(lambda row:
                                                    abs(row['key'] - key) + \
                                                    abs(row['tempo'] - tempo) + \
                                                    abs(row['loudness'] - loudness),
                                                    axis=1)
        return self.music.sort_values(['difference', 'artist.popularity', 'popularity'],
                                      ascending=[True, False, False]).head(amount)


if __name__ == "__main__":
    pd.set_option('display.max_columns', 15)
    test = MusicRecommendation()
    # print(test.get_songs_for_mood('frantic')[['title', 'artist.name', 'difference']])
    # print(test.get_songs_for_mood('energetic')[['title', 'artist.name']])
    print(test.get_songs_for_mood('depression')[['title', 'artist.name', 'difference']])
