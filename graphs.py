import matplotlib.pyplot as plt
import math
import numpy as np

def generate_time_graph(title, time_list, nodes):
    plt.figure(figsize=(10, 4))
    plt.plot(nodes, time_list)
    plt.xlabel('Liczba wierzchołków')
    plt.ylabel('Czas [s]')
    plt.title(title)
    plt.show()

def generate_dist_graph(title, distance_list, nodes):
    l = []
    for i in range(len(distance_list)):
        l.append(i)
    plt.figure(figsize=(10, 4))
    plt.plot(l, distance_list)
    plt.xlabel('Liczba zmian punktu początkowego')
    plt.ylabel('Dystans [km]')
    formated_title = title + ' dla n=' + str(nodes[0])
    plt.title(formated_title)
    plt.xticks(np.arange(len(l)))
    plt.show()

def generate_possible_paths_graph():
    poss_path = []
    num_nodes = []

    for i in range(3, 101):
        num_nodes.append(i)
        result = math.factorial(int(i) - 1) / 2
        poss_path.append(result)
        
    plt.figure(figsize=(6, 6))
    plt.semilogy(num_nodes, poss_path)
    plt.xlabel('Liczba wierzchołków')
    plt.ylabel('Liczba możliwych ścieżek')
    plt.xticks(np.arange(3, 101, step=4), rotation=45)
    plt.xlim(3, 100)
    plt.show()
