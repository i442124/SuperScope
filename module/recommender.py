import math
import numpy as np
import pandas as pd

from storage import games
from storage import ratings

from sklearn.cluster import KMeans
from sklearn.impute import KNNImputer
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

import matplotlib
import matplotlib.pyplot as plt
plt.style.use('seaborn')

## NUBMER OF CLUSTERS THAT THE 
## REVIEWERS SHOULD BE DEVIDED INTO
K_CLUSTERS = 11

## SCORE REDUCTION STRENGTH FOR GAMES
## WITH LOWER AMOUNT OF REVIEWS IN
## THE CLUSTER
PENALIZER_STRENGTH = 1

## HOW TO RESOLVE NAN VALUES FOR
## CRITICS THAT HAVEN"T PLAYED A GENRE
## POSSIBLE CHOICES: 'drop', 'mean', 'zeros', 'neutral' and 'kNN'
IMPUTATION_RESOLVER = 'kNN'

def avg_genre_matrix(ratings):
    # Split each game into multiple rows
    # for each genre they have, this makes
    # it easier to cacluate the average score
    genre_ratings = pd.merge(games, ratings)
    genre_ratings = genre_ratings.explode(column='genres')

    # Calcluate average of each review_critic for each genre
    genre_ratings = genre_ratings.groupby(['review_critic', 'genres']).mean()
    genre_ratings = genre_ratings.reset_index().pivot('review_critic', 'genres', 'meta_score')
    return genre_ratings

def avg_genre_matrix_weighted(ratings):
    # Split each game into multiple rows
    # for each genre they have, this makes
    # it easier to calculate the average weighted score
    genre_ratings = pd.merge(games, ratings)
    genre_ratings = genre_ratings.explode(column='genres')

    # Calculate the average score and count the 
    # total amount of ratings of each review_critic 
    # for each genre they have played/reviewed
    genre_ratings = genre_ratings.groupby(['review_critic', 'genres']).agg({'genres':'size', 'meta_score':'mean'})
    genre_ratings = genre_ratings.rename(columns={'genres': 'count' }).reset_index()

    # Next, we need to calculate the min, max and sum of reviews for each critic
    # in order to properly weigh the different ratings for each genre the have played
    genre_ratings['sum'] = genre_ratings.groupby(['review_critic'])['count'].transform('sum')
    genre_ratings['min'] = genre_ratings.groupby(['review_critic'])['count'].transform('min')
    genre_ratings['max'] = genre_ratings.groupby(['review_critic'])['count'].transform('max')

    # We need to weigh our meta_score based on the amount of reviews in the genre,
    # while also taking into account the total amount of reviews the critic has written
    # Basically, a single rating of 90 in one genre should be lowered 
    # compared to ten ratings with 85 in on average in another genre
    genre_ratings['weighted_score'] = genre_ratings['count'] / (genre_ratings['count'] + (genre_ratings['max'] - genre_ratings['min']) / genre_ratings['sum']) * genre_ratings['meta_score']
    genre_ratings = genre_ratings.reset_index().pivot('review_critic', 'genres', 'weighted_score')
    return genre_ratings

# Imputates missing values in a datafarme
# 'drop', removes rows with missing values
# 'zeros', fills all missing values with zero
# 'neutral', fills all missing values with fifty
# 'mean', fills all missing values with the average score
# 'kNN', fills all missing values with the nearest neighbors
def impute_missing_values(genre_ratings, imputer=IMPUTATION_RESOLVER):
    if imputer == 'drop':
        return genre_ratings.dropna()
    elif imputer == 'zeros':
        return genre_ratings.fillna(value=0)
    elif imputer == 'neutral':
        return genre_ratings.fillna(value=50)
    elif imputer == 'mean':
        return genre_ratings.fillna(genre_ratings.mean())
    elif imputer == 'kNN':
        imputer = KNNImputer(n_neighbors=5, weights='uniform', metric='nan_euclidean')
        return pd.DataFrame(imputer.fit_transform(genre_ratings), columns=genre_ratings.columns, index=genre_ratings.index)

# Looks for clusters in all ratings
def find_clusters(ratings, k=K_CLUSTERS, imputer=IMPUTATION_RESOLVER):

    # Create a (weighted) genre matrix and
    # impute the missing values if necessary
    genre_ratings = avg_genre_matrix_weighted(ratings)
    genre_ratings = impute_missing_values(genre_ratings, imputer)

    # Standardize the input values to avoid 
    # miscalculations in the distance of data
    SS = StandardScaler(with_mean=True, with_std=True)
    trainX = SS.fit_transform(genre_ratings)

    # Cluster all the reviewers
    clusterer = KMeans(n_clusters=k, random_state=42)
    clusters = clusterer.fit_predict(trainX)
    
    # Add clusters to the matrix 
    # dataframe of the genre reviews
    genre_ratings['cluster'] = clusters
    genre_ratings = genre_ratings.reset_index()

    # Add clusters to the orignal dataframe and return
    return ratings.merge(genre_ratings[['review_critic', 'cluster']])

def find_clusters_debug(ratings, k=K_CLUSTERS, imputer=IMPUTATION_RESOLVER):

    # Create a (weighted) genre matrix and
    # impute the missing values if necessary
    genre_ratings = avg_genre_matrix_weighted(ratings)
    genre_ratings = impute_missing_values(genre_ratings, imputer)

    # Standardize the input values to avoid 
    # miscalculations in the distance of data
    SS = StandardScaler(with_mean=True, with_std=True)
    trainX = SS.fit_transform(genre_ratings)

    # Cluster all the reviewers
    clusterer = KMeans(n_clusters=k, random_state=42)
    clusters = clusterer.fit_predict(trainX)
    
    # Add clusters to the matrix 
    # dataframe of the genre reviews
    genre_ratings['cluster'] = clusters
    genre_ratings = genre_ratings.reset_index()

    # Add clusters to the orignal dataframe and return
    return ratings.merge(genre_ratings[['review_critic', 'cluster']])


# Looks for the best reviewed game in a cluster
def get_recommendation_scores(ratings, cluster, penalizer_strength=PENALIZER_STRENGTH):

    # Filter the ratings to the specified cluster
    # and group all the results by platform and title
    cluster = ratings[ratings['cluster'] == cluster]
    cluster = cluster.groupby(['platform', 'title'])
    
    # Calculate the average score of all critics and count
    # the amount of reviews written for each title release
    cluster = cluster.agg(count=('title', 'size'), meta_score=('meta_score', 'mean'))
    cluster = cluster.reset_index()

    # Create method to weigh the amount of review with the review score,
    # in order to get more balanced results between quantity and quality
    weigh = lambda x: (x['count'])/(x['count'] + penalizer_strength) * x['meta_score']

    # Copy the cluster dataframe and add
    # an additional recommendation score for    
    # each game in the cluster
    recommendations = pd.DataFrame(cluster)
    recommendations['recommendation_score'] = weigh(cluster)
    return recommendations.sort_values(['recommendation_score'], ascending=False)

# Plots all clusters on a radar to see how
# each cluster differs from the others in
# regard to preferences of certain genres
def plot_cluster_genres(genre_ratings, genres):

    # select the genres we want to spectate and
    # group all the entires into their own cluster
    radar = genre_ratings[genres.tolist() + ['cluster']]
    radar = radar.groupby('cluster').mean()
    radar = radar.reset_index()
    radar.columns.name = None

    # calculate the numbers of
    # rows and columns required
    ncols = int(round(math.sqrt(len(radar.index))))
    nrows = int(math.ceil(len(radar.index)/ncols))

    # select a color palette to use for the differnet clusters
    my_palette = plt.cm.get_cmap('rainbow', len(radar.index))

    # initialize figure
    plt.figure(figsize=(ncols*2.4, nrows*2.4))
    plt.subplots_adjust(hspace=0.6)

    # loop through all the different clusters
    # and plot the radar of the different genres
    for idx, row in radar.iterrows():

        # get current color
        color = my_palette(idx)

        # calculate the different angles for all the labels based
        # on the number of genres that we want to display (eg. 0°, 90°, 180°, 270°)
        angles = [n / float(len(genres)) * 2 * math.pi for n in range(len(genres))]
        angles += angles[:1]

        # create the subplot and set the 
        # theta offset and direction
        ax = plt.subplot(nrows, ncols, idx+1, polar=True)
        ax.set_theta_offset(math.pi / 2)
        ax.set_theta_direction(-1)

        # get the values from the current row
        values = row.values[1:].flatten().tolist()
        values += values[:1]

        # plot the values onto the radar
        ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
        ax.fill(angles, values, color=color, alpha=0.4)
        ax.set_rlabel_position(7)

        # set ticks, labels ant titles
        plt.xticks(angles[:-1], genres, size=11, color='grey')    
        plt.yticks(range(0, 100 + 20, 20), size=8, color="grey")
        plt.title(f"Cluster {int(row.cluster)}", size=13, color=color)


# Plots the amount of critics
# in a cluster on a bar chart 
def plot_critics_in_cluster(genre_ratings):
    genre_ratings['cluster'].value_counts().plot.bar()
    plt.title('Amount of critics in cluster')
    plt.ylabel('Amount of critics')
    plt.xlabel('Cluster')
    plt.xticks(rotation=0)

# Plots the amount of reviews
# in a cluster on a bar chart
def plot_reviews_in_cluster(ratings):
    ratings['cluster'].value_counts().plot.bar()
    plt.title('Amount of reviews in cluster')
    plt.ylabel('Amount of reviews')
    plt.xlabel('Cluster')
    plt.xticks(rotation=0)
