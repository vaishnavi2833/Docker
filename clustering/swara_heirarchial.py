import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy

df = pd.read_csv('data.csv')
df.sort_values(by='Weight', inplace=True)
X = df[['Weight']].values

def distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

def create_distance_matrix(X):
    n = X.shape[0]
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            distance_matrix[i, j] = distance(X[i], X[j])
            distance_matrix[j, i] = distance_matrix[i, j]
    return distance_matrix

def closest_clusters(distance_matrix):
    min_dist = np.inf
    cluster_pair = (None, None)
    for i in range(len(distance_matrix)):
        for j in range(i + 1, len(distance_matrix)):
            if distance_matrix[i, j] < min_dist:
                min_dist = distance_matrix[i, j]
                cluster_pair = (i, j)
    return cluster_pair, min_dist

n_samples = X.shape[0]
clusters = [[i] for i in range(n_samples)]
distance_matrix = create_distance_matrix(X)

print("Initial Distance Matrix:")
print(distance_matrix)
print("Initial Clusters:", clusters)

dendrogram_data = []

while len(clusters) > 1:
    cluster_pair, min_dist = closest_clusters(distance_matrix)
    dendrogram_data.append([cluster_pair[0], cluster_pair[1], min_dist])

    new_cluster = (X[cluster_pair[0]] + X[cluster_pair[1]]) / 2
    X = np.vstack([X, new_cluster])

    distance_matrix = np.delete(distance_matrix, cluster_pair, axis=0)
    distance_matrix = np.delete(distance_matrix, cluster_pair, axis=1)

    new_distances = []
    for i in range(len(distance_matrix)):
        new_distance = distance(X[i], new_cluster)
        new_distances.append(new_distance)

    distance_matrix = np.vstack([distance_matrix, new_distances])
    distance_matrix = np.column_stack([distance_matrix, np.append(new_distances, 0)])

    clusters.append(clusters[cluster_pair[0]] + clusters[cluster_pair[1]])

    del clusters[max(cluster_pair)]
    del clusters[min(cluster_pair)]

    print(f"Distance Matrix after merging clusters {cluster_pair}:")
    print(distance_matrix)
    print("Current Clusters:", clusters)
    print()

dendrogram_data = np.array(dendrogram_data)
Z = hierarchy.linkage(dendrogram_data, method='single')

plt.figure(figsize=(12, 6))
dn = hierarchy.dendrogram(Z)
plt.title('Dendrogram of Hierarchical Clustering (Score)')
plt.xlabel('Sample Index')
plt.ylabel('Distance')
plt.xticks(rotation=90)
plt.show()