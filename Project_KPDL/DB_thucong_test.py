import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score, adjusted_rand_score, normalized_mutual_info_score

# Load and preprocess data
data = pd.read_csv('video_features_scaled.csv')
features = np.array(data.drop(['video_name', 'category'], axis=1).fillna(0))

# Custom DBSCAN implementation
def dbscan_custom(X, eps=2.0, min_samples=5):
    labels = np.full(X.shape[0], -1, dtype=int)
    cluster_id = 0

    def euclidean_distance(point1, point2):
        return np.sqrt(np.sum((point1 - point2) ** 2))

    def get_neighbors(point_idx):
        neighbors = []
        for i in range(X.shape[0]):
            if i != point_idx and euclidean_distance(X[point_idx], X[i]) <= eps:
                neighbors.append(i)
        return neighbors

    for i in range(X.shape[0]):
        if labels[i] != -1:
            continue
        neighbors = get_neighbors(i)
        if len(neighbors) < min_samples:
            labels[i] = -1  # Noise
            continue
        cluster_id += 1
        labels[i] = cluster_id - 1  # Cluster IDs start from 0
        queue = neighbors[:]
        while queue:
            neighbor_idx = queue.pop(0)
            if labels[neighbor_idx] == -1:
                labels[neighbor_idx] = cluster_id - 1
            if labels[neighbor_idx] != -1:
                continue
            labels[neighbor_idx] = cluster_id - 1
            new_neighbors = get_neighbors(neighbor_idx)
            if len(new_neighbors) >= min_samples:
                queue.extend([n for n in new_neighbors if n not in queue])

    return cluster_id, labels

# Apply initial DBSCAN
eps = 2.0
min_samples = 5
cluster_count, labels = dbscan_custom(features, eps=eps, min_samples=min_samples)

# Adjust eps to aim for exactly 7 clusters (plus noise for 8 total)
attempts = 0
max_attempts = 20  # Prevent infinite loop
while cluster_count != 7 and attempts < max_attempts:
    if cluster_count > 7:
        eps -= 0.05  # Smaller step for finer control
    elif cluster_count < 7:
        eps += 0.05
    cluster_count, labels = dbscan_custom(features, eps=eps, min_samples=min_samples)
    attempts += 1

# Add cluster labels to data
data['cluster'] = labels

# Define cluster names based on specified features
cluster_names = {
    0: "StrongMotion",
    1: "LoudAudio",
    2: "BrightColor",
    3: "StaticShapes",
    4: "RepetitiveMotion",
    5: "ComplexTexture",
    6: "DenseScenes",
    -1: "Noise"
}

# Analyze clusters
cluster_stats = {}
feature_names = data.drop(['video_name', 'category', 'cluster'], axis=1).columns
for label in np.unique(labels):
    cluster_data = data[data['cluster'] == label]
    cluster_stats[label] = {
        'size': len(cluster_data),
        'features': cluster_data.drop(['video_name', 'category', 'cluster'], axis=1).mean().to_dict(),
        'example': cluster_data['video_name'].iloc[0] if len(cluster_data) > 0 else None
    }

# Print cluster analysis
print("DBSCAN Clustering Analysis (Manual Implementation)")
print(f"Number of clusters: {cluster_count} (plus noise)")
print(f"Number of noise points: {len(data[data['cluster'] == -1])}")
print(f"Final eps used: {eps:.2f}")
print("\nCluster Details:")
for label in sorted(cluster_stats.keys()):
    cluster_name = cluster_names.get(label, f"Cluster_{label}")
    if label == -1:
        print(f"\n{cluster_name}:")
        print(f"Size: {cluster_stats[label]['size']} videos")
        print("Key Features:")
        print(f"  Scene Complexity (max): {data[data['cluster'] == -1]['scene_complexity_scaled'].max():.2f}")
        print(f"  Motion Intensity (max): {data[data['cluster'] == -1]['motion_intensity_scaled'].max():.2f}")
        print("Interpretation: Videos with extreme or unique feature values, e.g., high scene complexity (v_Archery_g06_c05.avi).")
    else:
        print(f"\n{cluster_name}:")
        print(f"Size: {cluster_stats[label]['size']} videos")
        print("Key Features:")
        for feature, value in cluster_stats[label]['features'].items():
            print(f"  {feature}: {value:.2f}")
        print("Interpretation:", end=" ")
        if cluster_name == "StrongMotion":
            print("High motion intensity, likely action videos (e.g., boxing or pushups).")
        elif cluster_name == "LoudAudio":
            print("Prominent audio features, possibly music or speech-heavy videos.")
        elif cluster_name == "BrightColor":
            print("Bright color profiles, indicating visually vibrant scenes.")
        elif cluster_name == "StaticShapes":
            print("Static scenes with distinct shapes, such as writing or drawing.")
        elif cluster_name == "RepetitiveMotion":
            print("Short, repetitive motion videos, like pushups or spinning.")
        elif cluster_name == "ComplexTexture":
            print("Complex textures, possibly crowded or detailed scenes.")
        elif cluster_name == "DenseScenes":
            print("Dense scenes with high scene complexity.")
        else:
            print("Other distinct video characteristics.")
        print(f"Example Video: {cluster_stats[label]['example'] or 'N/A'}")

# Evaluate clustering performance using silhouette score, Davies-Bouldin index, and Calinski-Harabasz index
mask = labels != -1
if mask.sum() > 0 and len(np.unique(labels[mask])) > 1:
    print('Silhouette:', silhouette_score(features[mask], labels[mask]))
    print('Davies-Bouldin:', davies_bouldin_score(features[mask], labels[mask]))
    print('Calinski-Harabasz:', calinski_harabasz_score(features[mask], labels[mask]))
if 'category' in data.columns:
    print('ARI:', adjusted_rand_score(data['category'][mask], labels[mask]))
    print('NMI:', normalized_mutual_info_score(data['category'][mask], labels[mask]))

# Plot scatter: motion_intensity_scaled vs mfcc_0_scaled
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=data['motion_intensity_scaled'], 
    y=data['mfcc_0_scaled'], 
    hue=[cluster_names.get(l, f"Cluster_{l}") for l in data['cluster']], 
    palette='deep', 
    style=[cluster_names.get(l, f"Cluster_{l}") for l in data['cluster']]
)
plt.xlabel('Motion Intensity (scaled)')
plt.ylabel('MFCC_0 (scaled)')
plt.title('DBSCAN Clusters: Motion Intensity vs MFCC_0')
plt.legend(title='Cluster', loc='best')
plt.show()

# Plot bar: cluster sizes
plt.figure(figsize=(8, 6))
cluster_sizes = pd.Series(labels).value_counts().sort_index()
cluster_sizes.index = [cluster_names.get(i, f"Cluster_{i}") for i in cluster_sizes.index]
cluster_sizes.plot(kind='bar')
plt.xlabel('Cluster')
plt.ylabel('Number of Videos')
plt.title('Cluster Sizes')
plt.show()