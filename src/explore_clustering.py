import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from load_data.prepocessing.data_cleaning import handle_categorical_OH

districts = pd.read_csv("ds/district.csv")
districts["unemploymant rate '95"].fillna(value=districts["unemploymant rate '95"].mean(), inplace=True)
districts["no. of commited crimes '95"].fillna(value=districts["no. of commited crimes '95"].mean(), inplace=True)

districts = handle_categorical_OH(districts, ["name", "region"])
districts = districts.loc[:, "no. of inhabitants":]

N_max = 30
n = [i for i in range(2, N_max)]
k_value = []
for i in range(2, N_max):
    kmeans = KMeans(n_clusters=i)
    districts["Cluster"] = kmeans.fit_predict(districts)
    districts["Cluster"] = districts["Cluster"].astype("category")

    score = silhouette_score(districts, kmeans.labels_, metric='euclidean')

    k_value.append(score)


plt.figure(figsize=(10, 5))
plt.plot(n, k_value)

plt.title("Evolution of Silhouette Coefficient with k value")
plt.ylabel("Silhouette Coefficient")
plt.xlabel("K Value")
plt.xticks(n)
plt.show()
