import itertools
import math
import time
import numpy as np
import random
from collections import deque
import timeit
import pygame

### Func to calculate distance between two points ###
def calc_distance(p1, p2):
    # Funkcja obliczająca odległość między dwoma punktami
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def distance_matrix(points):
    n = len(points)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i][j] = np.linalg.norm(
                np.array(points[i]) - np.array(points[j]))
    return matrix

### Brute Force Alg ###
def brute_force(coordinates):
    pos_paths = []
    start_time = time.time()
    starting_point = coordinates[0]
    coordinates = coordinates[1:]
    perm = list(itertools.permutations(coordinates))

    shortest_distance = float("inf")
    shortest_path = None

    for p in perm:
        distance = 0
        current_point = starting_point
        for i in range(len(p)):
            next_point = p[i]
            distance += math.sqrt((current_point[0]-next_point[0])
                                  ** 2 + (current_point[1]-next_point[1])**2)
            current_point = next_point
        distance += math.sqrt((current_point[0]-starting_point[0])
                              ** 2 + (current_point[1]-starting_point[1])**2)
        pos_paths.append([starting_point] + list(p) + [starting_point])

        if distance < shortest_distance:
            shortest_distance = distance
            shortest_path = [starting_point] + list(p) + [starting_point]

    return shortest_distance, time.time()-start_time, shortest_path, pos_paths

def nearest_neighbor(coordinates):
    start_time = timeit.default_timer()
    n = len(coordinates)
    visited = [False] * n
    path = [None] * n
    current = 0
    visited[current] = True
    path[0] = coordinates[current]
    total_distance = 0

    for i in range(1, n):
        nearest_neighbor_dist = math.inf
        for j in range(n):
            if not visited[j]:
                dist = math.sqrt((coordinates[current][0] - coordinates[j][0]) ** 2 +
                                 (coordinates[current][1] - coordinates[j][1]) ** 2)
                if dist < nearest_neighbor_dist:
                    nearest_neighbor_dist = dist
                    next_city = j
        visited[next_city] = True
        path[i] = coordinates[next_city]
        total_distance += nearest_neighbor_dist
        current = next_city

    total_distance += math.sqrt((coordinates[current][0] - coordinates[0][0]) ** 2 +
                                (coordinates[current][1] - coordinates[0][1]) ** 2)

    execution_time = timeit.default_timer() - start_time
    return execution_time, total_distance, path

### GENETIC ALG ###
def fitness(route, cities):
    total_distance = 0
    for i in range(len(route)):
        j = (i + 1) % len(route)
        city_i = cities[route[i]]
        city_j = cities[route[j]]
        total_distance += calc_distance(city_i, city_j)
    return total_distance

def crossover(parent1, parent2):
    # Choose two random crossover points
    cxpoint1 = random.randint(0, len(parent1) - 1)
    cxpoint2 = random.randint(0, len(parent1) - 1)
    if cxpoint2 < cxpoint1:
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Create a set to keep track of selected cities
    selected_cities = set(parent1[cxpoint1:cxpoint2])

    # Create a new child route by adding cities from parent2
    child = [city for city in parent2 if city not in selected_cities]

    # Insert the cities from parent1 into the child route
    child[cxpoint1:cxpoint1] = parent1[cxpoint1:cxpoint2]

    return child

def mutation(route, mutation_rate):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]
    return route

def genetic_alg(coords, population_size=200, generations=1000, mutation_rate=0.01, crossover_rate=0.8):
    start_time = time.time()

    # Create the initial population
    population = []
    for i in range(population_size):
        route = list(range(len(coords)))
        random.shuffle(route)
        population.append(route)

    # Evolve the population
    for i in range(generations):
        # Evaluate the fitness of each individual
        fitness_values = []
        for j in range(population_size):
            fitness_values.append(fitness(population[j], coords))

        # Select the parents for the next generation
        parents = []
        for j in range(population_size):
            parent1 = random.choices(population, weights=fitness_values, k=1)[0]
            parent2 = random.choices(population, weights=fitness_values, k=1)[0]
            parents.append((parent1, parent2))

        # Create the next generation
        new_population = []
        for j in range(population_size):
            parent1, parent2 = parents[j]

            if random.random() < crossover_rate:
                child = crossover(parent1, parent2)
            else:
                child = parent1

            child = mutation(child, mutation_rate)
            new_population.append(child)

        population = new_population

    # Find the best route
    best_route = population[0]
    best_fitness = fitness(best_route, coords)
    for route in population:
        route_fitness = fitness(route, coords)
        if route_fitness < best_fitness:
            best_route = route
            best_fitness = route_fitness

    end_time = time.time()

    def map_indices_to_coords(indices):
        return [coords[i] for i in indices]
    
    pos_paths = [map_indices_to_coords(route) for route in population]
    pos_paths_without_duplicates = np.unique(pos_paths, axis=0)

    return end_time - start_time, best_fitness, [coords[i] for i in best_route], pos_paths_without_duplicates.tolist()

### ANT ALG ###
def ant_colony_optimization(coordinates, n_ants=50, n_iterations=1000, evaporation_rate=0.5, alpha=1, beta=2, q=100, init_pheromone=1):
    n_cities = len(coordinates)
    distances = np.zeros((n_cities, n_cities))
    pheromones = np.ones((n_cities, n_cities)) * init_pheromone

    for i in range(n_cities):
        for j in range(i+1, n_cities):
            distances[i][j] = calc_distance(coordinates[i], coordinates[j])
            distances[j][i] = distances[i][j]

    shortest_distance = float('inf')
    shortest_path = []

    start_time = time.time()
    for i in range(n_iterations):
        positions = np.zeros((n_ants, n_cities), dtype=int)
        for j in range(n_ants):
            positions[j][0] = random.randint(0, n_cities-1)

        for j in range(1, n_cities):
            for k in range(n_ants):
                current_city = positions[k][j-1]
                unvisited_cities = [x for x in range(
                    n_cities) if x not in positions[k][:j]]
                probabilities = np.zeros(len(unvisited_cities))

                for idx, next_city in enumerate(unvisited_cities):
                    probabilities[idx] = (pheromones[current_city][next_city]**alpha) * (
                        1 / (distances[current_city][next_city] + 1e-10))**beta

                probabilities /= probabilities.sum()
                next_city_idx = np.random.choice(
                    range(len(unvisited_cities)), p=probabilities)
                next_city = unvisited_cities[next_city_idx]
                positions[k][j] = next_city

        distances_travelled = np.zeros(n_ants)
        for j in range(n_ants):
            for k in range(n_cities-1):
                distances_travelled[j] += distances[positions[j]
                                                    [k]][positions[j][k+1]]
            distances_travelled[j] += distances[positions[j]
                                                [-1]][positions[j][0]]

        delta_pheromones = np.zeros((n_cities, n_cities))
        for j in range(n_ants):
            for k in range(n_cities-1):
                delta_pheromones[positions[j][k]][positions[j]
                                                  [k+1]] += q / distances_travelled[j]
            delta_pheromones[positions[j][-1]][positions[j]
                                               [0]] += q / distances_travelled[j]

        pheromones = pheromones * evaporation_rate + delta_pheromones

        shortest_idx = np.argmin(distances_travelled)
        if distances_travelled[shortest_idx] < shortest_distance:
            shortest_distance = distances_travelled[shortest_idx]
            shortest_path = [coordinates[i] for i in positions[shortest_idx]]

    total_time = time.time() - start_time
    total_distance = shortest_distance

    pos_paths = []
    for pos in positions:
        path = [coordinates[i] for i in pos]
        pos_paths.append(path)
    pos_paths_without_duplicates = np.unique(pos_paths, axis=0)

    return total_time, total_distance, shortest_path, pos_paths_without_duplicates.tolist()

### ANT ALG ###
def calculate_path_distance(path, points):
    distance = 0
    for i in range(len(path)):
        point1 = points[path[i]]
        point2 = points[path[(i + 1) % len(path)]]
        distance += calc_distance(point1, point2)
    return distance

def generate_initial_solution(points):
    path = list(range(len(points)))
    random.shuffle(path)
    return path

def convert_path_to_points(path, points):
    return [points[i] for i in path]

def apply_2opt_move(path, i, j):
    new_path = path[:i]
    new_path.extend(reversed(path[i:j + 1]))
    new_path.extend(path[j + 1:])
    return new_path

def tabu_search(points, max_iterations=10, tabu_size=10):
    pos_paths = []
    pos_current = []
    start_time = time.time()

    # Generowanie rozwiązania początkowego
    current_path = generate_initial_solution(points)
    best_path = current_path.copy()
    best_distance = calculate_path_distance(current_path, points)

    # Inicjalizacja listy Tabu
    tabu_list = []

    # Główna pętla algorytmu
    iteration = 0
    while iteration < max_iterations:
        iteration += 1

        # Wybieranie najlepszego ruchu spośród sąsiedztwa
        best_move = None
        best_move_distance = float('inf')
        for i in range(len(current_path)):
            for j in range(i + 1, len(current_path)):
                move = apply_2opt_move(current_path, i, j)
                move_distance = calculate_path_distance(move, points)
                if move_distance < best_move_distance and move not in tabu_list:
                    best_move = move
                    best_move_distance = move_distance

        # Jeśli nie znaleziono lepszego ruchu, przerwij pętlę
        if best_move is None:
            break

        # Aktualizacja bieżącej ścieżki
        current_path = best_move
        
        # Aktualizacja najlepszego rozwiązania
        if best_move_distance < best_distance:
            best_path = best_move
            best_distance = best_move_distance



        # Dodanie ruchu do listy Tabu
        tabu_list.append(best_move)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

    for n in tabu_list:
        pos_current_path = convert_path_to_points(n, points)
        pos_current.append(pos_current_path)


    end_time = time.time()
    execution_time = end_time - start_time
    best_path_points = convert_path_to_points(best_path, points)

    return execution_time, best_distance, best_path_points, pos_current

### Simulated Annealing ###
def total_distance(points, order):
    distance_sum = 0
    for i in range(len(order)):
        distance_sum += calc_distance(points[order[i]],
                                 points[order[(i + 1) % len(order)]])
    return distance_sum

def simulated_annealing(points, temp=10000, cooling_rate=0.003):
    pos_paths = []
    order = list(range(len(points)))
    random.shuffle(order)
    current_distance = total_distance(points, order)
    shortest_distance = current_distance
    shortest_order = order[:]
    start_time = time.time()
    while temp > 1:
        i, j = random.sample(range(len(points)), 2)
        new_order = order[:]
        new_order[i], new_order[j] = new_order[j], new_order[i]
        new_distance = total_distance(points, new_order)
        delta_distance = new_distance - current_distance
        acceptance_probability = math.exp(-delta_distance / temp)
        if delta_distance < 0 or random.random() < acceptance_probability:
            order = new_order[:]
            current_distance = new_distance
            order_points = [points[i] for i in order]
            pos_paths.append(order_points)
        if current_distance < shortest_distance:
            shortest_distance = current_distance
            shortest_order = order[:]            
        temp *= 1 - cooling_rate

    shortest_path = [points[i] for i in shortest_order]

    end_time = time.time()

    return end_time - start_time, shortest_distance, shortest_path, pos_paths

### Depth Search Alg ###
def depth_search(points):
    start_time = time.time()
    n = len(points)
    visited = [False] * n
    path = []
    min_distance = float('inf')
    best_path = []
    all_paths = []

    def dfs(node, distance, count, all_paths):
        nonlocal min_distance, best_path

        visited[node] = True
        path.append(node)

        if count == n - 1:
            if distance + calc_distance(points[node], points[0]) < min_distance:
                min_distance = distance + calc_distance(points[node], points[0])
                best_path = path[:]
                all_paths.append(path[:])
        else:
            for next_node in range(n):
                if not visited[next_node]:
                    new_distance = distance + calc_distance(points[node], points[next_node])
                    dfs(next_node, new_distance, count + 1, all_paths)

        visited[node] = False
        path.pop()

    dfs(0, 0, 0, all_paths)
    execution_time = time.time() - start_time
    path_coordinates = [[points[i] for i in path] for path in all_paths]
    return execution_time, min_distance, [points[i] for i in best_path], path_coordinates

### Breadth-First Search ###
def bfs(coordinates):
    num_points = len(coordinates)
    best_path = None
    best_distance = float('inf')
    all_paths = []

    start_time = time.time()

    # Tworzenie grafu pełnego (wszystkie pary punktów)
    graph = [[0] * num_points for _ in range(num_points)]
    for i in range(num_points):
        for j in range(i+1, num_points):
            distance = calc_distance(coordinates[i], coordinates[j])
            graph[i][j] = distance
            graph[j][i] = distance

    # BFS
    queue = deque([(i, [i]) for i in range(num_points)])  # Kolejka rozpoczynająca się od każdego punktu
    while queue:
        current_node, path = queue.popleft()
        if len(path) == num_points:
            # Jeśli znaleziono pełną ścieżkę
            distance = sum(graph[path[i]][path[i+1]] for i in range(num_points-1))
            distance += graph[path[-1]][path[0]]  # Dodanie dystansu powrotu do punktu początkowego
            if distance < best_distance:
                best_distance = distance
                best_path = [coordinates[node] for node in path]  # Zwracanie listy współrzędnych
            all_paths.append([coordinates[node] for node in path])
        else:
            for next_node in set(range(num_points)) - set(path):
                queue.append((next_node, path + [next_node]))

    return time.time()-start_time, best_distance, best_path, all_paths

### Held-Karp Alg ###
def held_karp(points):
    start_time = time.time()

    # Liczba wszystkich punktów
    n = len(points)

    # Utworzenie słownika do przechowywania podproblemów
    dp = {}
    analysed_paths = {}

    # Inicjalizacja wartości dla podproblemów o rozmiarze 1
    for k in range(1, n):
        dp[(1 << k, k)] = (calc_distance(points[0], points[k]), 0)
        analysed_paths[(1 << k, k)] = [points[0], points[k]]

    # Iteracyjne obliczanie wartości dla większych podproblemów
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            for k in subset:
                prev_bits = bits ^ (1 << k)
                best_distance = float('inf')
                best_prev = None

                for m in subset:
                    if m == 0 or m == k:
                        continue

                    distance = dp[(prev_bits, m)][0] + calc_distance(points[m], points[k])
                    if distance < best_distance:
                        best_distance = distance
                        best_prev = m

                dp[(bits, k)] = (best_distance, best_prev)
                # Zapisywanie analizowanych ścieżek
                analysed_paths[(bits, k)] = list(analysed_paths[(prev_bits, best_prev)]) + [points[k]]

    # Obliczenie ostatecznego wyniku
    bits = (2 ** n - 1) - 1
    best_distance = float('inf')
    best_prev = None

    for k in range(1, n):
        distance = dp[(bits, k)][0] + calc_distance(points[k], points[0])
        if distance < best_distance:
            best_distance = distance
            best_prev = k

    # Odtworzenie najkrótszej ścieżki
    path = [0]
    k = best_prev
    bits = (2 ** n - 1) - 1

    for _ in range(n - 1):
        path.append(k)
        prev = k
        k = dp[(bits, prev)][1]
        bits ^= (1 << prev)

    path.append(0)

    # Zwrócenie czasu wykonania algorytmu, najkrótszej odległości oraz najkrótszej ścieżki
    elapsed_time = time.time() - start_time
    path_points = [points[i] for i in path]
    analysed_paths = [list(path) for path in analysed_paths.values()]

    return elapsed_time, best_distance, path_points, analysed_paths


################################################################