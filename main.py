import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

pd.set_option('display.expand_frame_repr', False)
data = pd.read_csv("movies.csv")
movieTitle = data['title']
yearList = dict()
yearListTemp = dict()


def movies_per_year():
    for title in movieTitle:
        year = re.search("\\(([0-9]+)\\)$", title.strip())
        if year:
            y = int(year.group(1))
            if y in yearList:
                yearList[y] += 1
            else:
                yearList[y] = 1
    for year in sorted(yearList.keys()):
        yearListTemp[year] = yearList[year]
    plt.plot(list(yearListTemp.keys()), list(yearListTemp.values()))
    plt.xticks(np.arange(min(yearListTemp.keys()), max(yearListTemp.keys()) + 10, 10), rotation=60)
    plt.show()


# function calls
movies_per_year()