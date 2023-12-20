import os
import json

def update_json_data(file_name, data):
    if not os.path.exists(file_name) or os.stat(file_name).st_size == 0:
        dict = [data]
    else:
        with open(file_name, 'r') as file:
            dict = json.load(file)
            dict.append(data)
    
    with open(file_name, 'w') as file:
        json.dump(dict, file, indent=4)

def get_json_time_data(file_name, value):
    time = []
    nodes = []
    with open(file_name, 'r') as plik:
        data = json.load(plik)

    for dict in data:
        if "alg_name" in dict and dict["alg_name"] == value:
            time.append(dict["time"])
            nodes.append(dict["nodes_amount"])            

    return time, nodes

def get_json_dist_data(file_name, value):
    distance = []
    nodes = []
    with open(file_name, 'r') as plik:
        data = json.load(plik)

    for dict in data:
        if "alg_name" in dict and dict["alg_name"] == value:
            distance.append(dict["distance"])
            nodes.append(dict["nodes_amount"])            

    return distance, nodes
