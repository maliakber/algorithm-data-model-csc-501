import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from wordcloud import WordCloud, STOPWORDS  # used to generate world cloud
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')
pd.set_option('mode.chained_assignment', None)

startTime = time.time()
movies = pd.read_csv("20M/movies.csv")
ratings = pd.read_csv("20M/ratings.csv")
# links = pd.read_csv("20M/links.csv")
tags = pd.read_csv("20M/tags.csv")
# genomeScores = pd.read_csv("20M/genome-scores.csv")
# genomeTags = pd.read_csv("20M/genome-tags.csv")
print("It took %s seconds to load the data" % (time.time() - startTime))

# CLEAN AND FORMAT
startTime = time.time()
tags = tags.dropna()
movies['year'] = movies['title'].str.extract('\\(([0-9]+)\\)$', expand=False)
movies = movies.dropna()  # removing the null values
movies['year'] = movies['year'].astype(int)
moviesGenres = movies[['year','genres']].copy()
del movies['genres']
del ratings['timestamp']
del ratings['userId']
del tags['timestamp']
del tags['userId']

# join operations
movies_tags = pd.merge(movies[['movieId', 'title']], tags['movieId'], on='movieId')
movies_ratings_year = pd.merge(movies[['movieId', 'year']], ratings[['movieId', 'rating']], on='movieId')
movies_ratings_title = pd.merge(movies[['movieId', 'title']], ratings[['movieId', 'rating']], on='movieId')


def movies_per_year():
    movie_year_count = movies.groupby('year').count()['movieId']
    plt.figure(figsize=(10, 5))
    plt.plot(movie_year_count)
    plt.xticks(np.arange(1890, 2015 + 10, 10), rotation=60)
    plt.grid()
    plt.ylabel("Number of Movies")
    plt.xlabel("Year")
    plt.title("Movie Distribution By Year")
    plt.show()


def ratings_per_year():
    avg_rating = movies_ratings_year.groupby('year').rating.mean()
    plt.figure(figsize=(10, 5))
    plt.plot(avg_rating)
    plt.xticks(np.arange(1890, 2015 + 10, 10), rotation=60)
    plt.yticks(np.arange(1.5, 5.5, 0.5))
    plt.ylabel("Average Rating")
    plt.xlabel("Year")
    plt.title("Average Movie Rating By Year")
    plt.grid()
    plt.show()


def movies_per_genre():
    moviesGenreCount = dict()
    for val in moviesGenres['genres'].values:
        for genre in val.strip().split('|'):
            if genre in moviesGenreCount:
                moviesGenreCount[genre] += 1
            else:
                moviesGenreCount[genre] = 1
    x, y = moviesGenreCount.keys(), moviesGenreCount.values()  # unpack a list of pairs into two tuples
    plt.figure(figsize=(10, 5))
    plt.bar(x, y, width=1.0, facecolor=(0.2, 0.4, 0.6, 0.6), edgecolor='blue')
    plt.xticks(rotation=80)
    plt.yticks(np.arange(min(y), max(y) + 1000, 1000))
    plt.ylabel("Number of Movies")
    plt.xlabel("Genre")
    plt.title("Movie Distribution By Genre")
    plt.show()
    return x


def genre_per_year():
    fig = plt.figure(figsize=(30, 30))
    index = 1
    for genre in diffMovieGenres:
        filtered_result = moviesGenres[moviesGenres['genres'].str.contains(genre)]
        result = filtered_result.groupby('year')['genres'].count().reset_index(name="count")
        ax = fig.add_subplot(5, 4, index)
        result.plot(x='year', y='count', title=genre, c=np.random.rand(3, ), ax=ax)
        index += 1


# define a function that counts the number of times each tag appear
def tags_data_parse():
    tag_count = dict()
    for tag in tags['tag']:
        tag = tag.lower()
        if tag in tag_count:
            tag_count[tag] += 1
        else:
            tag_count[tag] = 1
    tag_count = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)
    return tag_count


# Function that control the color of the words
def random_color_func(word=None, font_size=None, position=None,
                      orientation=None, font_path=None, random_state=None):
    tone = 100  # define the color of the words
    h = int(360.0 * tone / 255.0)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(70, 120)) / 255.0)
    return "hsl({}, {}%, {}%)".format(h, s, l)


def show_most_tagged():
    tag_count = dict(tags_data_parse()[0:50])
    f, ax = plt.subplots(figsize=(15, 6))
    wordcloud = WordCloud(width=550, height=300, background_color='black',
                          max_words=50, relative_scaling=0.6,
                          color_func=random_color_func,
                          normalize_plurals=True)
    wordcloud.generate_from_frequencies(tag_count)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()


def movie_with_most_tags():
    title_count = movies_tags.groupby('title')["movieId"].count().reset_index(name="count")
    title_count = title_count.sort_values('count', ascending=False)[0:15]
    title_count.plot.bar(x='title', y='count', width=1.0, facecolor=(0.2, 0.4, 0.6, 0.6), edgecolor='blue',
                         figsize=(10, 5), rot=85)


def movie_with_most_user_rating():
    rating_count = movies_ratings_title.groupby(['title'])['movieId'].count().to_frame('count').reset_index()
    avg_rating = movies_ratings_title.groupby(['title'])['rating'].mean().to_frame('avgRating').reset_index()
    most_rated_movies = rating_count.sort_values('count', ascending=False)[0:15]
    top_avg_rating = pd.merge(most_rated_movies[['title','count']], avg_rating[['title','avgRating']], on='title')
    top_avg_rating.plot.bar(x='title', y='count', ylim=(45000, 68000),
                            width=1.0, figsize=(10,5), facecolor=(0.2, 0.4, 0.6, 0.6), edgecolor='blue', rot=85)
    top_avg_rating.plot.bar(x='title', y='avgRating', ylim=(min(top_avg_rating.avgRating)-0.2, max(top_avg_rating.avgRating)+0.2),
                            width=1.0, figsize=(10,5), facecolor=(0.2, 0.4, 0.6, 0.6), edgecolor='blue', rot=85)
    top_avg_rating[['count']] = top_avg_rating[['count']].apply(lambda x: (x - x.min() + 1000) / (x.max() - x.min()))
    top_avg_rating[['avgRating']] = top_avg_rating[['avgRating']].apply(lambda x: (x - x.min() + .05) / (x.max() - x.min()))
    top_avg_rating.plot.bar(x='title', y=['count','avgRating'], figsize=(10,5), rot=85)


def rating_summary():
    avg_rating = ratings.groupby('rating')['movieId'].count()
    avg_rating.plot(grid=True, figsize=(10, 5), color='blue')


def space_time_cube():
    result = movies_ratings_year.groupby(['year', 'rating'])['movieId'].count().reset_index(name='count')
    fig = plt.figure(figsize=(10, 5))
    ax = Axes3D(fig)
    x = result['year']
    y = result['rating']
    z = result['count']
    ax.scatter(x, y, z, s=40, c='blue', marker='x')


movies_per_year()
ratings_per_year()
diffMovieGenres = movies_per_genre()
genre_per_year()
show_most_tagged()
movie_with_most_tags()
movie_with_most_user_rating()
rating_summary()
space_time_cube()

print("It took %s seconds to process the data" % (time.time() - startTime))