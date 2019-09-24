import time
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

startTime = time.time()
movies = pd.read_csv("20M/movies.csv")
ratings = pd.read_csv("20M/ratings.csv")
links = pd.read_csv("20M/links.csv")
tags = pd.read_csv("20M/tags.csv")
genomeScores = pd.read_csv("20M/genome-scores.csv")
genomeTags = pd.read_csv("20M/genome-tags.csv")
print("It took %s seconds to load the data" % (time.time() - startTime))

moviesYearCount = {}  # dictionary to store movies count per year
moviesGenreCount = {}  # dictionary to store movies count per genre


def split_movies_data(title, genres):
    for i in range(len(title)):
        year = re.search("\\(([0-9]+)\\)$", title[i].strip())
        if year:
            y_int = int(year.group(1))
            if y_int in moviesYearCount:
                moviesYearCount[y_int] += 1
            else:
                moviesYearCount[y_int] = 1
        for genre in genres[i].strip().split('|'):
            if genre in moviesGenreCount:
                moviesGenreCount[genre] += 1
            else:
                moviesGenreCount[genre] = 1


def split_movies_year():
    for title in movies['title']:
        year = re.search("\\(([0-9]+)\\)$", title.strip())
        if year:
            y_int = int(year.group(1))
            if y_int in moviesYearCount:
                moviesYearCount[y_int] += 1
            else:
                moviesYearCount[y_int] = 1


def split_movies_genre():
    for genres in movies['genres']:
        genres = genres.strip().split('|')
        for genre in genres:
            if genre in moviesGenreCount:
                moviesGenreCount[genre] += 1
            else:
                moviesGenreCount[genre] = 1


def movies_per_year():
    x, y = zip(*sorted(moviesYearCount.items()))  # unpack a list of pairs into two tuples
    plt.plot(x, y)
    plt.xticks(np.arange(min(x), max(x) + 10,  10), rotation=60)
    plt.yticks(np.arange(min(y), max(y) + 100, 100))
    plt.grid()
    plt.ylabel("Number of Movies")
    plt.xlabel("Year")
    plt.title("Movie Distribution By Year")
    plt.show()


def movies_per_genre():
    x, y = moviesGenreCount.keys(), moviesGenreCount.values()  # unpack a list of pairs into two tuples
    plt.bar(x, y, width=1.0, facecolor=(0.2, 0.4, 0.6, 0.6), edgecolor='blue')
    plt.xticks(rotation=80)
    plt.yticks(np.arange(min(y), max(y) + 1000, 1000))
    plt.ylabel("Number of Movies")
    plt.xlabel("Genre")
    plt.title("Movie Distribution By Genre")
    plt.show()


# function calls
# split_movies_year()
# split_movies_genre()
startTime = time.time()
split_movies_data(movies['title'].values, movies['genres'].values)
# movies_per_year()
movies_per_genre()
print("It took %s seconds to process the data" % (time.time() - startTime))