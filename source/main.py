import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from wordcloud import WordCloud, STOPWORDS  # used to generate world cloud

pd.set_option('mode.chained_assignment', None)

startTime = time.time()
movies = pd.read_csv("20M/movies.csv")
ratings = pd.read_csv("20M/ratings.csv")
links = pd.read_csv("20M/links.csv")
tags = pd.read_csv("20M/tags.csv")
# genomeScores = pd.read_csv("20M/genome-scores.csv")
# genomeTags = pd.read_csv("20M/genome-tags.csv")
print("It took %s seconds to load the data" % (time.time() - startTime))

tags = tags.dropna()
del ratings['timestamp']
del tags['timestamp']

movies['year'] = movies['title'].str.extract('\\(([0-9]+)\\)$', expand=False)
movies = movies.dropna()

movies['year'] = movies['year'].astype(int)  # sorting separately after cleaning data, cause there can be null values
movies = movies.sort_values(by='year')


def movies_per_year():
    movie_year_count = movies.groupby('year').count()['movieId']
    plt.plot(movie_year_count)
    plt.xticks(np.arange(1890, 2015 + 10, 10), rotation=60)
    plt.grid()
    plt.ylabel("Number of Movies")
    plt.xlabel("Year")
    plt.title("Movie Distribution By Year")
    # plt.show()


def ratings_per_year():
    result = pd.merge(movies[['movieId', 'year']], ratings[['movieId', 'rating']], on='movieId')
    avg_rating = result.groupby('year').rating.mean()
    plt.plot(avg_rating)
    plt.xticks(np.arange(1890, 2015 + 10, 10), rotation=60)
    plt.ylabel("Average Rating")
    plt.xlabel("Year")
    plt.title("Average Movie Rating By Year")
    plt.grid()
    # plt.show()


def movies_per_genre():
    moviesGenreCount = dict()
    for val in movies['genres'].values:
        for genre in val.strip().split('|'):
            if genre in moviesGenreCount:
                moviesGenreCount[genre] += 1
            else:
                moviesGenreCount[genre] = 1
    x, y = moviesGenreCount.keys(), moviesGenreCount.values()  # unpack a list of pairs into two tuples
    plt.bar(x, y, width=1.0, facecolor=(0.2, 0.4, 0.6, 0.6), edgecolor='blue')
    plt.xticks(rotation=80)
    plt.yticks(np.arange(min(y), max(y) + 1000, 1000))
    plt.ylabel("Number of Movies")
    plt.xlabel("Genre")
    plt.title("Movie Distribution By Genre")
    # plt.show()


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
    f, ax = plt.subplots(figsize=(14, 6))
    cloud = WordCloud(width=550, height=300, background_color='black',
                      max_words=50, relative_scaling=0.6,
                      color_func=random_color_func,
                      normalize_plurals=True)
    cloud.generate_from_frequencies(tag_count)
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis('off')
    # plt.show()


def movie_with_most_tags():
    result = pd.merge(movies[['movieId', 'title']], tags['movieId'], on='movieId')
    title_count = result.groupby('title')["movieId"].count().reset_index(name="count")
    title_count = title_count.sort_values('count', ascending=False)[0:15]
    # title_count.plot.bar(x='title', y='count', width=1.0, facecolor=(0.2, 0.4, 0.6, 0.6), edgecolor='blue', rot=85)


def movie_with_most_user_rating():
    result = pd.merge(movies[['movieId', 'title']], ratings[['movieId', 'rating']], on='movieId')
    rating_count = result.groupby(['title'])['movieId'].count().to_frame('count').reset_index()
    avg_rating = result.groupby(['title'])['rating'].mean().to_frame('avgRating').reset_index()
    most_rated_movies = rating_count.sort_values('count', ascending=False)[0:15]
    top_avg_rating = pd.merge(most_rated_movies[['title', 'count']], avg_rating[['title', 'avgRating']], on='title')
    # top_avg_rating.plot.bar(x='title', y='count', ylim=(45000, 68000), width=1.0, facecolor=(0.2, 0.4, 0.6, 0.6), edgecolor='blue', rot=85)
    # top_avg_rating.plot.bar(x='title', y='avgRating', ylim=(min(top_avg_rating.avgRating)-0.2, max(top_avg_rating.avgRating)+0.2), width=1.0, facecolor=(0.2, 0.4, 0.6, 0.6), edgecolor='blue', rot=85)
    top_avg_rating[['count']] = top_avg_rating[['count']].apply(lambda x: (x - x.min() + 1000) / (x.max() - x.min()))
    top_avg_rating[['avgRating']] = top_avg_rating[['avgRating']].apply(
        lambda x: (x - x.min() + .05) / (x.max() - x.min()))
    # top_avg_rating.plot.bar(x='title', y=['count','avgRating'], rot=85)


def rating_summary():
    result = ratings.groupby('rating')['movieId'].count()
    # result.plot(grid=True, color='blue')


# function calls
startTime = time.time()

rating_summary()
movie_with_most_user_rating()
movie_with_most_tags()
show_most_tagged()
movies_per_genre()
ratings_per_year()
movies_per_year()

print("It took %s seconds to process the data" % (time.time() - startTime))
