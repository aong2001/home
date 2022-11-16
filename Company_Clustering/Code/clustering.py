import json
import pandas as pd
import itertools
import numpy as np

def cluster_finder(max_miles, distances_dict): 
    '''
    Finds clusters of firms to each other based on milage input.
    '''
    cik_clusters = []
    for cik1 in distances_dict.keys():  # iterate through all the distances of each point to each other
        calculated_distances = distances_dict[cik1]
        
        close_ciks = []
        for distance_pair in calculated_distances: 
            cik2 = distance_pair[0]
            distance2 = float(distance_pair[1])

            if distance2 < max_miles:  # 
                close_ciks.append(str(cik2))

        close_ciks.append(cik1)
        if len(close_ciks) != 1: 
            cik_clusters.append(close_ciks)
        else: 
            continue

    sorted_cik_clusters = []
    for cluster in cik_clusters: 
        dedup_cluster = list(set(cluster))
        sorted_cluster = sorted(dedup_cluster, key = int)
        sorted_cik_clusters.append(sorted_cluster)

    dedup_cik_clusters = []
    for cluster in sorted_cik_clusters: 
        if cluster not in dedup_cik_clusters:
            dedup_cik_clusters.append(cluster)

    return dedup_cik_clusters

def cluster_overlap(lst_clusters): 
    '''
    Find and combine clusters that overlap with each other.
    '''
    needs_iteration = True
    working_clusters = lst_clusters
    unique_ciks = len(set([cik for cluster in lst_clusters for cik in cluster]))

    while needs_iteration:
        original_clusters = len(working_clusters)
        
        for idx1, cluster1 in enumerate(working_clusters): 
            for idx2, cluster2 in enumerate(working_clusters): 
                if idx1 == idx2:
                    continue
                similiar_ratio = len(set(cluster1) & set(cluster2)) / unique_ciks

                if similiar_ratio > 0.05: 
                    merged_clusters = list(set(cluster1 + cluster2))
                    to_exclude = [idx1, idx2]
                    new_working_clusters = [clst for idx, clst in enumerate(working_clusters) if idx not in to_exclude]

                    new_working_clusters.append(merged_clusters)
                    working_clusters = new_working_clusters
                    break

            else: 
                continue 
            break
        
        new_clusters = len(working_clusters)
        if new_clusters == original_clusters: 
            needs_iteration = False
                
    return working_clusters
                
def cluster_information(lst_clusters): 
    '''
    Finds information about each cluster.
    '''

    length_clusters = [len(cluster) for cluster in lst_clusters]
    avg_length_clusters = round(np.average(length_clusters), 3)
    
    return avg_length_clusters

file_path = 'usa_cik_distances.json'
with open(file_path) as json_file:
    distance_data = json.load(json_file)

# can alter distances as neccesary
r_clusters = cluster_finder(50, distance_data)
c_clusters = cluster_overlap(r_clusters)

export_path = 'clustered_busines_50m.json'
with open(export_path, 'w') as json_file: 
    json.dump(c_clusters, json_file)
