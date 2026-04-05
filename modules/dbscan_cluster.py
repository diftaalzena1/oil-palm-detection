# modules/dbscan_cluster.py
import numpy as np
from sklearn.cluster import DBSCAN

def apply_dbscan(boxes_all, eps_factor, img_h, img_w):
    """Apply DBSCAN clustering on bounding box centroids."""
    centroids = np.array([[(x1+x2)/2, (y1+y2)/2] for (x1,y1,x2,y2) in boxes_all])
    box_sizes = np.array([max(x2-x1, y2-y1) for (x1,y1,x2,y2) in boxes_all])
    avg_size = np.mean(box_sizes)
    eps = eps_factor * avg_size
    db = DBSCAN(eps=eps, min_samples=1).fit(centroids)
    labels = db.labels_
    unique_labels = set(labels)
    total_trees = len(unique_labels)
    final_centroids = [centroids[labels == l].mean(axis=0) for l in unique_labels]
    coords = [[int(cx), int(cy)] for cx, cy in final_centroids]
    return total_trees, coords