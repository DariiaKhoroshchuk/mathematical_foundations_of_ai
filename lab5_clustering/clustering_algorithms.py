from random import random
import matplotlib.pyplot as plt


def distance(a1, b1, a2, b2):
    return pow(pow(a1-a2, 2) + pow(b1-b2, 2), .5)


def init_arr(n):
    return [(random(), random()) for _ in range(n)]


def k_mean(arr, k):
    def calc_centers(cts):
        data = [[0, 0, 0] for _ in range(k)] # 0: sumX, 1: sumY, 2: count
        for idx, point in enumerate(arr):
            data[cts[idx]][0] += point[0]
            data[cts[idx]][1] += point[1]
            data[cts[idx]][2] += 1
        for idx, item in enumerate(data):
            data[idx] = (item[0] / item[2], item[1] / item[2]) # 0: centerX, 1: centerY
        return data

    def update_clusters(centers):
        cts = []
        for point in arr:
            min_sum = 2
            min_idx = 0
            for idx, c in enumerate(centers):
                d = distance(point[0], point[1], c[0], c[1])
                if d < min_sum:
                    min_sum = d
                    min_idx = idx
            cts.append(min_idx)
        return cts
    centers = [(random(), random()) for _ in range(k)]
    clusters = update_clusters(centers)
    centers = calc_centers(clusters)
    new_clusters = update_clusters(centers)
    while new_clusters != clusters:
        clusters = new_clusters
        centers = calc_centers(clusters)
        new_clusters = update_clusters(centers)
    return new_clusters


def hierarchical(arr):
    N = len(arr)
    clusters = [i for i in range(N)]
    distances = [
            {"i": i, "j": i+j+1, "d": distance(arr[i][0], arr[i][1], arr[i+j+1][0], arr[i+j+1][1])}
            for i in range(N) for j in range(N-i-1)]
    distances.sort(key=lambda x: x.get("d"))
    i = 0 
    counter = 0
    while counter < N-1:
        item = distances[i]
        i += 1
        ctr = clusters[item.get("i")]
        remove = clusters[item.get("j")]
        if ctr == remove:
            continue
        if item.get("d") > 1.2/(1e3**.5):
            break
        for j in range(N):
            if clusters[j] == remove:
                clusters[j] = ctr
        counter += 1
    types = list(set(clusters))
    print(len(types))
    type_map = {}
    for i, t in enumerate(types):
        type_map[t] = i
    for i in range(N):
        clusters[i] = type_map.get(clusters[i])
    return clusters, len(types)


def plot_clusters(arr, cts1, k, cts2, n):
    fig, axs = plt.subplots(2)
    fig.suptitle('K mean VS hierarchical clustering')
    for i in range(k):
        data = [t for (idx, t) in enumerate(arr) if cts1[idx] == i]
        axs[0].scatter([p[0] for p in data], [p[1] for p in data])
    for i in range(n):
        data = [t for (idx, t) in enumerate(arr) if cts2[idx] == i]
        axs[1].scatter([p[0] for p in data], [p[1] for p in data])

    
arr = init_arr(1000)
clusters1 = k_mean(arr, 5)
clusters2, n = hierarchical(arr)
plot_clusters(arr, clusters1, 5, clusters2, n)
