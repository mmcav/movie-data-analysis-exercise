# -*- coding: utf-8 -*-
"""movies_analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1j55CHILernaK5Ri5sPuo0ZGRqEQVBl-v

In this exercise, I will go through a movie dataset extracted from The Movie Database website, [provided by the Kaggle user 'asaniczka'](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies/), and see what kinds of insights that can be extracted by applying some basic descriptive statistics.
"""

import pandas as pd

df = pd.read_csv('tmdb_movie_dataset.csv')

df.head()

"""First things first: I loaded the data from a CSV file into a pandas dataframe."""

print(df.info())
print(df.isnull().sum())

"""Since I can't assure that the data is clean and ready for any kind of analysis, it is a good practice to probe it, see what kind of data it contains, what are its columns, and whether it contains null values."""

print(f'Total number of movies: {len(df)}')
print(f'Number of movies without an average vote value: {len(df[df.vote_average == 0])}')
print(f'Number of movies without a vote count value: {len(df[df.vote_count == 0])}')
print(f'Number of movies without a release date: {len(df[df.release_date.isnull()])}')
not_released = len(df[df.status != 'Released'])
print(f'Number of movies without a \'Released\' status: {not_released}')
print(f'Number of movies with an \'adult\' flag (aka, pornographic movies): {len(df[df.adult])}')

"""Considering that many of the analyses that will be made later depends on voting data and release date data, it is useful to filter the dataframe based on those parameters. I'm also not interested in movies flagged as "adult" or movies that might be flagged as "not released"."""

df_filtered = df[(df.vote_average != 0) &
                 (df.vote_count != 0) &
                 ~(df.release_date.isnull()) &
                 (df.adult == False) &
                 (df.status == 'Released')]
df_filtered['release_date'] = pd.to_datetime(df_filtered['release_date'], format='%Y-%m-%d')
print(df_filtered.info())
print(df_filtered.isnull().sum())

"""On top of filtering the dataframe, I've also changed the release date from a string data type to a datetime data type. I'm not sure why just yet, but personally I believe it is good practice, that doing so could avoid future issues."""

df_final = df_filtered.drop(columns=['status', 'adult', 'backdrop_path', 'homepage', 'overview', 'poster_path', 'tagline'])
df_final = df_final.drop(columns=['imdb_id', 'original_language', 'original_title', 'popularity', 'genres', 'production_companies', 'production_countries', 'spoken_languages', 'keywords'])
print(df_final.info())
print(df_final.isnull().sum())

"""The original dataframe included a lot of data that are mostly useless, like backdrop path and poster path, so I dropped those columns.

I spotted a couple of more columns that could potentially generate some interesting insights, like production companies or TMDB's own popularity metric. But for the purposes of this exercise those were also deemed not necessary and dropped as well.
"""

df_final.iloc[:, 1:].describe().drop('count')

"""A few things stand out right from the start, just by looking at the dataframe "describe table":

- There is a significant difference between the vote count's third quartile (75%) and its max value.
- The runtime's maximum value is considerably bigger than the third quartile.

But before we get into those points, one other detail stood out...
"""

df_final.sort_values(by='revenue', ascending=False).head(5)

"""While probing the data, I stumbled upon this movie called... "TikTok Rizz Party"??? Upon further review, it appears to be an internet meme that at some point was added to TMDB, perhaps jokingly. It has since been deleted from the website, so it's probably safe to delete it from my dataframe."""

df_final = df_final.drop(df_final[df_final.id == 1270893].index.values[0])

"""Begone!

Moving on...
"""

df_final.sort_values(by='runtime', ascending=False).head(10)

"""Regarding the apparent runtime value discrepancies mentioned earlier, upon review, the data seems to be correct. These movies with seemingly very large runtimes do exist. They're mostly experimental movies and documentaries.

Not quite the type of insight that I initially thought I was going to extract from this dataset, but it is still an insight nonetheless.
"""

import matplotlib.pyplot as plt

"""To produce the graphs in this exercise, I used the matplotlib library."""

df_final.sort_values(by='vote_count', ascending=False).head(10).drop(columns=['id'])

"""First, I wanted to look at the vote count, starting with the movies that have the most votes on TMDB. The vote count in this top 10 list is in the 25000 to 35000 value range."""

plt.figure(figsize=(10, 6))
plt.hist(df_final['vote_count'], bins=100, edgecolor='black', alpha=0.7)
plt.xlabel('Vote Count')
plt.ylabel('Frequency')
plt.title('Distribution of Vote Counts')
plt.grid(True)
plt.show()

"""Putting all the data in a histogram graph shows that a large amount of movies on TMDB have very few votes. Looking back at the "describe table", the median value for this data column sits at 6 votes, which is very distant from the values seen at the top 10 list produced previously."""

plt.figure(figsize=(8, 6))
plt.boxplot(df_final['vote_count'], vert=True)
plt.xlabel('Vote Count')
plt.title('Box Plot of Vote Counts')
plt.grid(True)
plt.show()

"""This box plot illustrates the discrepancies seen in the "describe table" and the previous graph. The box that represents the values inside the first and third quartile is barely visible."""

plt.figure(figsize=(10, 6))
plt.hist(df_final[df_final.vote_count >= 1000]['vote_count'], bins=100, edgecolor='black', alpha=0.7)
plt.xlabel('Vote Count')
plt.ylabel('Frequency')
plt.title('Distribution of Vote Counts\n(Excluding Values Below 1000 Votes)')
plt.grid(True)
plt.show()

"""To make the visualization easier, in this graph I limited the data to movies that have at least 1000 votes. It shows that very few movies manage to break into a five-digit number. Even if you go lower, such as 5000 votes, it is still a threshold too high for most.

A very large portion of movie titles exists unseen to the majority of the website's users.
"""

plt.figure(figsize=(10, 6))
plt.hist(df_final['vote_average'], bins=100, edgecolor='black', alpha=0.7)
plt.xlabel('Vote Average')
plt.xticks(range(0, 11))
plt.ylabel('Vote Count')
plt.title('Distribution of Vote Averages')
plt.grid(True)
plt.show()

"""Next, I looked at the vote average data. The number of movies rated 10 stand out. Can there really be that many movies with a "perfect rating"?

Of course not. A quick reminder that an average with a low number of samples makes this metric easy to manipulate. And, as seen previously, there is a significant number of movie titles with a very low vote count.
"""

plt.figure(figsize=(10, 6))
plt.hist(df_final[df_final.vote_count >= 1000]['vote_average'], bins=100, edgecolor='black', alpha=0.7)
plt.xlabel('Vote Average')
plt.xticks(range(0, 11))
plt.ylabel('Vote Count')
plt.title('Distribution of Vote Averages\n(For Movies With 1000 Votes or More)')
plt.grid(True)
plt.show()

"""Using the value 1000 as the minimum number of votes, the graph for the vote average distribution becomes quite different. A large portion of movies that received at least that many votes sit near the 7/10 rating range.

Most users do not use the full rating scale. One could assume that they do not bother watching or rating movies that they wouldn't consider at least "good" or even "passable" in the first place.
"""

top_revenue = df_final.sort_values(by='revenue', ascending=False).head(20)

plt.figure(figsize=(12, 8))
plt.barh(top_revenue['title'], top_revenue['revenue'], alpha=0.7, edgecolor='black')
plt.xlabel('Revenue (In Billions of Dollars)')
plt.ylabel('Movie Title')
plt.title('Top 20 Movies by Revenue')
plt.gca().invert_yaxis()
plt.grid(True)
plt.show()

"""Moving on to the revenue. James Cameron's Avatar and Marvel's Endgame stand out above the rest, but otherwise there is very little surprises here.

I wonder how revenue compares to the ROI (return of investment) metric.
"""

import numpy as np
df_final['roi'] = df_final['revenue'] / df_final['budget']
df_final = df_final.replace([np.inf, -np.inf], np.nan).dropna(subset=['roi'])

top_roi = df_final.sort_values(by='roi', ascending=False).head(20)

plt.figure(figsize=(12, 8))
plt.barh(top_roi['title'], top_roi['roi'], alpha=0.7, edgecolor='black')
plt.xlabel('ROI')
plt.ylabel('Movie Title')
plt.title('Top 20 Movies by Return on Investment (ROI)')
plt.gca().invert_yaxis()
plt.grid(True)
plt.show()

"""Hmm... Some rather unusual movies in this list. Could these really be the most lucrative movie titles?

Of course not. TMDB's data on budget and revenue might not be accurate for low popularity movies (as seen in the code above, I had to apply some quick fixes for cases where division by zero occurred). More popular movies have better chances of having more accurate data.
"""

top_roi = df_final[df_final.vote_count >= 1000].sort_values(by='roi', ascending=False).head(20)

plt.figure(figsize=(12, 8))
plt.barh(top_roi['title'], top_roi['roi'], alpha=0.7, edgecolor='black')
plt.xlabel('ROI')
plt.ylabel('Movie Title')
plt.title('Top 20 Movies by Return on Investment (ROI)\n(For Movies With 1000 Votes or More)')
plt.gca().invert_yaxis()
plt.grid(True)
plt.show()

"""Again, using the value 1000 vote count as the minimum, I drew the graph once more. This time, I actually recognize some of these titles! But it is still quite a different list compared to top revenue list.

This shouldn't come as a surprise. Some movie productions are made with very tight budgets and a few end up becoming worldwide phenomenoms. Low budgets and high revenues result in extremely high ROI's.
"""

plt.figure(figsize=(10, 6))
plt.scatter(df_final['budget'], df_final['revenue'], alpha=0.5, edgecolors='w', linewidth=0.5)
plt.xlabel('Budget')
plt.ylabel('Revenue')
plt.title('Budget vs. Revenue')
plt.xscale('log')
plt.yscale('log')
plt.axline((0, 0), (1, 1), color='red', linestyle='--')
plt.grid(True)
plt.show()

"""Speaking of budget, how does it compare to the revenue? For that, I drew a scatter plot to try to visualize a potential relationship between the two.

Overall, there seems to be an increase in revenue with the budget, as you can almost visualize an upward line (it kinda looks like an arrow, doesn't it). At lower budget values, the points are more spread out, indicating higher uncertainty in this relationship. At higher budget values, they are packed together, though a large number seems to fall below the profitability line (indicated by the red line).
"""

plt.figure(figsize=(10, 6))
plt.scatter(df_final['budget'], df_final['vote_average'], alpha=0.5, edgecolors='w', linewidth=0.5)
plt.xlabel('Budget')
plt.ylabel('Vote Average')
plt.title('Budget vs. Vote Average')
plt.xscale('log')
plt.yticks(range(0, 11))
plt.grid(True)
plt.show()

"""Moving on, how does budget and vote average relate? Do higher budgets lead to higher votes on TMDB?

Well, this first graph is a mess. Again, too many movies with low vote counts.
"""

plt.figure(figsize=(10, 6))
plt.scatter(df_final[df_final.vote_count >= 1000]['budget'], df_final[df_final.vote_count >= 1000]['vote_average'], alpha=0.5, edgecolors='w', linewidth=0.5)
plt.xlabel('Budget')
plt.ylabel('Vote Average')
plt.title('Budget vs. Vote Average\n(For Movies With 1000 Votes or More)')
plt.xscale('log')
plt.yticks(range(0, 11))
plt.grid(True)
plt.show()

"""Once again setting the vote count limit to 1000.

The resulting graph doesn't appear to show any kind of linear tendency like my previous scatter plot attempt. There is seemingly a lot of movies with very high budgets getting both high and middling vote averages.

But it does show that the majority of the votes appear to go to movies with mid to high budgets. Based on this plot, a movie with a budget lower than a million dollars is considerably less likely to catch the eye of a TMDB user.
"""

avg_rating_by_year = df_final[df_final.vote_count >= 1000].groupby(df_final['release_date'].dt.year)['vote_average'].mean()
plt.figure(figsize=(12, 6))
plt.plot(avg_rating_by_year.index, avg_rating_by_year.values, marker='o', linestyle='-', color='royalblue')
plt.xlabel('Year')
plt.xticks(range(1900, 2030, 10))
plt.ylabel('Vote Average')
plt.title('Vote Average by Release Year\n(For Movies With 1000 Votes or More)')
plt.grid(True)
plt.show()

"""Lastly, I looked at the vote average grouped by release year. On a first look, it seems that TMDB users give higher ratings to older movies. Perhaps they treat newer movies more harshly? If that is really the case, then why is there an increase in vote average starting from 2010?

Yet another reminder that averages can be manipulated with a lower denominator. In this case, the denominator represents the number of released movies in each year.
"""

release_count_by_year = df_final[df_final.vote_count >= 1000].groupby(df_final['release_date'].dt.year).count()
plt.figure(figsize=(12, 6))
plt.plot(release_count_by_year.index, release_count_by_year.values, marker='o', linestyle='-', color='royalblue')
plt.xlabel('Year')
plt.xticks(range(1900, 2030, 10))
plt.ylabel('Release Count')
plt.title('Release Count by Release Year\n(For Movies With 1000 Votes or More)')
plt.grid(True)
plt.show()

"""And here is a graph showing the number of released movies grouped by year. The number of released movies goes into an upward trend, more visible around the 70's, and somwhere in the mid 2010 it goes down drastically. This trend goes against the one shown in the previous graph and can partially explain why certain time periods years have higher averages than others."""