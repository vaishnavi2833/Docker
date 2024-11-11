import pandas as pd
import numpy as np

df = pd.read_csv('./data.csv')
X = df[['Weight']].values

def distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

def centroid(cluster):
    points = [X[i] for i in flatten(cluster)]
    return np.mean(points, axis=0)

def flatten(cluster):
    if isinstance(cluster, list):
        return [item for sublist in cluster for item in flatten(sublist)]
    else:
        return [cluster]

def create_distance_matrix(clusters):
    n = len(clusters)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            distance_matrix[i, j] = distance(centroid(clusters[i]), centroid(clusters[j]))
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
distance_matrix = create_distance_matrix(clusters)
dendrogram_data = []

step = 1
while len(clusters) > 1:
    cluster_pair, min_dist = closest_clusters(distance_matrix)
    dendrogram_data.append([cluster_pair[0], cluster_pair[1], min_dist])

    new_cluster = [clusters[cluster_pair[0]], clusters[cluster_pair[1]]]
    clusters.append(new_cluster)

    print(f"Step {step}: Clusters formed: {clusters}")
    step += 1

    del clusters[max(cluster_pair)]
    del clusters[min(cluster_pair)]

    distance_matrix = np.delete(distance_matrix, cluster_pair, axis=0)
    distance_matrix = np.delete(distance_matrix, cluster_pair, axis=1)

    new_distances = []
    for i in range(len(distance_matrix)):
        new_distance = distance(centroid(clusters[i]), centroid(new_cluster))
        new_distances.append(new_distance)

    distance_matrix = np.vstack([distance_matrix, new_distances])
    distance_matrix = np.column_stack([distance_matrix, np.append(new_distances, 0)])

    print("Current Distance Matrix:")
    print(distance_matrix)
    print("\n")
