from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import mean_squared_error

import matplotlib
import matplotlib.pyplot as plt

def sum_squared_distance(trainX, k):
    clusterer = KMeans(n_clusters=k)
    clusterer.fit_predict(trainX)
    return clusterer.inertia_

def plot(trainX, possible_k_values):
    squared_distances = [sum_squared_distance(trainX, k) for k in possible_k_values]
    plt.plot(possible_k_values, squared_distances, marker='.', markersize=12)
    plt.xticks(range(min(possible_k_values), max(possible_k_values)+1))
    plt.title('Elbow method for optimal K')
    plt.ylabel('Sum of squared distances')
    plt.xlabel('Number of clusters')
