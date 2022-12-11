import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def get_possible_anomalies(curr_col):
    X_raw = curr_col.dropna()        
    X = np.array(X_raw).reshape(-1,1)
    X = StandardScaler().fit_transform(X)
    db = DBSCAN(eps=0.8, min_samples=10).fit(X)
    labels = db.labels_
    possible_outliers = list(X_raw[labels == -1])
    possible_outliers = [round(po, 4) for po in possible_outliers]
    possible_outliers.sort()
    return possible_outliers
