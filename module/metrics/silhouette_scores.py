from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import mean_squared_error

import matplotlib
import matplotlib.pyplot as plt

def calculate_score(trainX, k):
    clusterer = KMeans(n_clusters=k)
    preds = clusterer.fit_predict(trainX)
    return silhouette_score(trainX, preds)

def plot(trainX, possible_k_values):
    silhouette_scores = [calculate_score(trainX, k) for k in possible_k_values]
    plt.plot(possible_k_values, silhouette_scores, marker='.', markersize=12, color='red')
    plt.xticks(range(min(possible_k_values), max(possible_k_values)+1))
    plt.title('Silhouette score over the number of clusters')
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette scores')
