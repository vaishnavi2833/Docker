import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('./data.csv')
X = df[['Weight', 'Age']].values

K = 1 
max_iters = 10  

centroids = X[np.random.choice(X.shape[0], K, replace=False)]

def distance(X, centroids):
    distances = np.zeros((X.shape[0], centroids.shape[0])) 
    
    for i in range(centroids.shape[0]):
        for j in range(X.shape[0]):
            distances[j, i] = np.linalg.norm(X[j] - centroids[i]) 
    
    return distances

def assign_clusters(X, centroids):
    distances = distance(X, centroids)
    return np.argmin(distances, axis=1)

def update_centroids(X, clusters, K):
    new_centroids = np.array([X[clusters == k].mean(axis=0) for k in range(K)])
    return new_centroids

for i in range(max_iters):
    clusters = assign_clusters(X, centroids)
    
    print(f"Iteration {i+1}:")
    print(f"Centroids: \n{centroids}\n")
    
    new_centroids = update_centroids(X, clusters, K)
    
    if np.all(centroids == new_centroids):
        print(f"Convergence reached at iteration {i+1}")
        break
    
    centroids = new_centroids

plt.figure(figsize=(10, 6))
plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='viridis', s=100, label='Data points')
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=200, alpha=0.75, marker='X', label='Final Centroids')
plt.xlabel('Weight')
plt.ylabel('Age')
plt.title('Clustering Final Result (Weight and Age)')
plt.legend()
plt.show()
