import sys
import pygame
import math
import random


from coordinates import create_nodes
from algorithms import brute_force, nearest_neighbor, genetic_alg, ant_colony_optimization, tabu_search, simulated_annealing, depth_search, bfs, held_karp
from data_handler import update_json_data, get_json_time_data, get_json_dist_data
from graphs import generate_time_graph, generate_dist_graph, generate_possible_paths_graph
from coords import nodes100


WIN_WIDTH = 1500
WIN_HEIGHT = 850

BACKGROUND_COLOR = (51, 52, 64)
DEFAULT_COLOR = (200, 201, 163)
ELEMENT_COLOR = (90, 196, 106)
STARTING_POINT_COLOR = (255, 0, 34)
OTHER_POINT_COLOR = (0, 255, 13)
ALL_LINES_COLOR = (0, 0, 0)
BEST_LINES_COLOR = (0, 8, 255)
BTN_HIGHLIGHT_COLOR = (89, 90, 112)


class App:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('TSP Visualization')
        self.clock = pygame.time.Clock()

        self.slider_width = 300
        self.slider_height = 20
        self.slider_x = 30
        self.slider_y = 490
        self.slider_range = (3, 100)
        self.slider_value = 3

        self.pix_to_km = 1.144

        self.which_tab = 0

        self.generate_nodes = Button(40, 565, 130, 50, ["Generuj", "wierzchołki"])
        self.delete_nodes = Button(190, 565, 130, 50, ["Usuń", "wierzchołki"])
        self.change_starting_node = Button(40, 620, 280, 25, ["Zmień punkt startowy"])

        self.left_switch = Button(40, 680, 40, 40, ["<"], 30)
        self.right_switch = Button(280, 680, 40, 40, [">"], 30)

        self.left_switch_graph = Button(40, 460, 40, 40, ["<"], 30)
        self.right_switch_graph = Button(280, 460, 40, 40, [">"], 30)

        self.speed = ["B. szybko", "Szybko", "Normalnie"]
        self.which_speed = 0
        self.left_switch_speed = Button(40, 420, 40, 40, ["<"], 30)
        self.right_switch_speed = Button(280, 420, 40, 40, [">"], 30)

        self.algorithms = ["Brute Force", "Najbliższy sąsiad", "Genetyczny", "Mrówkowy", "Tabu Search", "Sym. Wyżarzanie", "Depth Search", "Breadth-First", "Held-Karp"]
        self.which_algorithm = 0
        self.which_algorithm_graphs = 0

        self.start = Button(125, 785, 100, 40, ["START"])
        self.get_time_data = Button(110, 520, 140, 40, ["START", "Czas"])
        self.get_distance_data = Button(110, 580, 140, 40, ["START", "Dystans"])
        self.get_possible_paths_data = Button(110, 640, 140, 40, ["START", "Możliwe ścieżki"])

        self.visualization = Button(50, 345, 120, 40, ["Wizualizacja"], color=BTN_HIGHLIGHT_COLOR)
        self.graphs = Button(200, 345, 100, 40, ["Wykresy"])

        self.save_time = Button(30, 735, 140, 40, ["Zapis - czas"])
        self.save_distance = Button(190, 735, 140, 40, ["Zapis - dystans"])

        self.is_save_time = False
        self.is_save_distance = False

        self.map = pygame.image.load("img/mapa.png")
        self.map_rect_coords = [585, 80, 1265, 760]

        self.points = []
        self.points_centers = []
        self.pos_paths = []
        self.pos_current = []

        self.distance = 0
        self.work_time = 0
        self.current_distance = 0
        self.pos_best_distance = math.inf
        self.pos_best_path = []
        self.shortest_path = []
        self.is_done = False
        self.is_alg_running = False

        self.alg_time = []
        self.alg_distance = []
        self.alg_nodes = []

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.slider_value == 3:
                            pass
                        else:
                            self.slider_value -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.slider_value == 100:
                            pass
                        else:
                            self.slider_value += 1
                    elif event.key == pygame.K_DOWN:
                        print('Generating nodes!')
                        # if self.which_algorithm == 0 and self.slider_value > 10:
                        #     pass
                        # else:
                        self.points_centers.clear()
                        self.shortest_path.clear()
                        self.work_time = 0
                        self.distance = 0
                        self.points = create_nodes(self.slider_value)
                        for tuple in self.points:
                            new_tuple = (tuple[0]+5, tuple[1]+5)
                            self.points_centers.append(new_tuple)
                        # self.points = self.chosen_points(self.slider_value)
                        # for tuple in self.points:
                        #     new_tuple = (tuple[0]+5, tuple[1]+5)
                        #     self.points_centers.append(new_tuple)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.which_tab == 0:
                            mouse_x, mouse_y = event.pos
                            if self.slider_x <= mouse_x <= self.slider_x + self.slider_width and self.slider_y <= mouse_y <= self.slider_y + self.slider_height:
                                self.slider_value = int((mouse_x - self.slider_x) / self.slider_width * (
                                    self.slider_range[1] - self.slider_range[0]) + self.slider_range[0])
                            if self.generate_nodes.handle_event(event):
                                print('Generating nodes!')
                                # if self.which_algorithm == 0 and self.slider_value > 10:
                                #     pass
                                # else:
                                self.points_centers.clear()
                                self.shortest_path.clear()
                                self.work_time = 0
                                self.distance = 0
                                self.pos_best_distance = math.inf
                                self.pos_best_path.clear()
                                self.current_distance = 0
                                self.points = create_nodes(self.slider_value)
                                for tuple in self.points:
                                    new_tuple = (tuple[0]+5, tuple[1]+5)
                                    self.points_centers.append(new_tuple)
                                # self.points = self.chosen_points(self.slider_value)
                                # for tuple in self.points:
                                #     new_tuple = (tuple[0]+5, tuple[1]+5)
                                #     self.points_centers.append(new_tuple)
                            if self.delete_nodes.handle_event(event):
                                print('Deleting nodes!')
                                self.points.clear()
                                self.points_centers.clear()
                                self.shortest_path.clear()
                                self.work_time = 0
                                self.distance = 0
                                self.win.blit(self.map, (585, 80))
                            if self.change_starting_node.handle_event(event):
                                self.shortest_path.clear()
                                self.work_time = 0
                                self.distance = 0
                                self.points = self.switch_starting_node(self.points)
                            if self.left_switch.handle_event(event):
                                self.switch_algorithm("left")
                            if self.right_switch.handle_event(event):
                                self.switch_algorithm("right")
                            if self.left_switch_speed.handle_event(event):
                                self.switch_speed("left")
                            if self.right_switch_speed.handle_event(event):
                                self.switch_speed("right")
                            if self.save_time.handle_event(event):
                                self.switch_boolean_time()
                            if self.save_distance.handle_event(event):
                                self.switch_boolean_dist()
                            if self.start.handle_event(event):
                                print("START")
                                self.is_alg_running = True
                                self.start_algorithm()
                                self.is_alg_running = False
                                self.is_done = False

                        if self.which_tab == 1:
                            if self.left_switch_graph.handle_event(event):
                                self.switch_algorithm_graph("left")
                            if self.right_switch_graph.handle_event(event):
                                self.switch_algorithm_graph("right")
                            if self.get_time_data.handle_event(event):
                                if self.algorithms[self.which_algorithm_graphs] == "Brute Force":
                                    self.alg_time, self.alg_nodes = get_json_time_data("data/time_data.json", "brute_force")                                   
                                    generate_time_graph("Brute Force", self.alg_time, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Najbliższy sąsiad":
                                    self.alg_time, self.alg_nodes = get_json_time_data("data/time_data.json", "nearest_neighbor")
                                    generate_time_graph("Najbliższy sąsiad", self.alg_time, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Genetyczny":
                                    self.alg_time, self.alg_nodes = get_json_time_data("data/time_data.json", "genetic")
                                    generate_time_graph("Genetyczny", self.alg_time, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Mrówkowy":
                                    self.alg_time, self.alg_nodes = get_json_time_data("data/time_data.json", "ant")
                                    generate_time_graph("Mrówkowy", self.alg_time, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Tabu Search":
                                    self.alg_time, self.alg_nodes = get_json_time_data("data/time_data.json", "tabu")
                                    generate_time_graph("Tabu Search", self.alg_time, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Sym. Wyżarzanie":
                                    self.alg_time, self.alg_nodes = get_json_time_data("data/time_data.json", "sim_ann")
                                    generate_time_graph("Symulowane Wyżarzanie", self.alg_time, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Depth Search":
                                    self.alg_time, self.alg_nodes = get_json_time_data("data/time_data.json", "depth")
                                    generate_time_graph("Depth Search", self.alg_time, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Breadth-First":
                                    self.alg_time, self.alg_nodes = get_json_time_data("data/time_data.json", "bfs")
                                    generate_time_graph("Breadth-First", self.alg_time, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Held-Karp":
                                    self.alg_time, self.alg_nodes = get_json_time_data("data/time_data.json", "held_karp")
                                    generate_time_graph("Held-Karp", self.alg_time, self.alg_nodes)
                            if self.get_distance_data.handle_event(event):
                                if self.algorithms[self.which_algorithm_graphs] == "Brute Force":
                                    self.alg_distance, self.alg_nodes = get_json_dist_data("data/distance_data.json", "brute_force")                                    
                                    generate_dist_graph("Brute Force", self.alg_distance, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Najbliższy sąsiad":
                                    self.alg_distance, self.alg_nodes = get_json_dist_data("data/distance_data.json", "nearest_neighbor")                                    
                                    generate_dist_graph("Najbliższy sąsiad", self.alg_distance, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Genetyczny":
                                    self.alg_distance, self.alg_nodes = get_json_dist_data("data/distance_data.json", "genetic")                                    
                                    generate_dist_graph("Genetyczny", self.alg_distance, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Mrówkowy":
                                    self.alg_distance, self.alg_nodes = get_json_dist_data("data/distance_data.json", "ant")                                    
                                    generate_dist_graph("Mrówkowy", self.alg_distance, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Tabu Search":
                                    self.alg_distance, self.alg_nodes = get_json_dist_data("data/distance_data.json", "tabu")                                    
                                    generate_dist_graph("Tabu Search", self.alg_distance, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Sym. Wyżarzanie":
                                    self.alg_distance, self.alg_nodes = get_json_dist_data("data/distance_data.json", "sim_ann")                                    
                                    generate_dist_graph("Symulowane Wyżarzanie", self.alg_distance, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Depth Search":
                                    self.alg_distance, self.alg_nodes = get_json_dist_data("data/distance_data.json", "depth")                                    
                                    generate_dist_graph("Depth Search", self.alg_distance, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Breadth-First":
                                    self.alg_distance, self.alg_nodes = get_json_dist_data("data/distance_data.json", "bfs")                                    
                                    generate_dist_graph("Breadth-First", self.alg_distance, self.alg_nodes)
                                elif self.algorithms[self.which_algorithm_graphs] == "Held-Karp":
                                    self.alg_distance, self.alg_nodes = get_json_dist_data("data/distance_data.json", "held_karp")                                    
                                    generate_dist_graph("Held-Karp", self.alg_distance, self.alg_nodes)
                            if self.get_possible_paths_data.handle_event(event):
                                generate_possible_paths_graph()
                        if self.visualization.handle_event(event):
                            self.which_tab = 0
                            self.visualization.color = BTN_HIGHLIGHT_COLOR
                            self.graphs.color = BACKGROUND_COLOR
                        
                        if self.graphs.handle_event(event):
                            self.which_tab = 1
                            self.graphs.color = BTN_HIGHLIGHT_COLOR
                            self.visualization.color = BACKGROUND_COLOR

            self.win.fill(BACKGROUND_COLOR)

            self.title_display()
            self.menu_display()

            self.win.blit(self.map, (585, 80))

            if len(self.points) > 0:
                self.draw_squares()

            if self.which_algorithm == 0 and len(self.shortest_path) > 0:
                if self.is_done == False:                    
                    for path in self.pos_paths:
                        self.draw_bf(path)
                        self.win.blit(self.map, (585, 80))
                        self.draw_squares()
                        pygame.display.update()
                        self.is_done = True
                pygame.draw.lines(self.win, BEST_LINES_COLOR,
                                      True, self.shortest_path)
                self.draw_best_distance_time()
            elif self.which_algorithm == 1 and len(self.shortest_path) > 0:
                if self.is_done == False:
                    self.draw_nn(self.shortest_path)
                    pygame.display.update()
                    self.is_done = True
                pygame.draw.lines(self.win, BEST_LINES_COLOR,
                        True, self.shortest_path)
                self.draw_best_distance_time()
            elif self.which_algorithm == 2 and len(self.shortest_path) > 0:
                if self.is_done == False:                    
                    for path in self.pos_paths:
                        self.draw_gen(path)
                        self.win.blit(self.map, (585, 80))
                        self.draw_squares()
                        if self.current_distance < self.pos_best_distance:
                            self.pos_best_distance = self.current_distance
                            self.pos_best_path.clear()
                            self.pos_best_path = path
                        if len(self.pos_best_path) > 0:
                            pygame.draw.lines(self.win, BEST_LINES_COLOR,
                                True, self.pos_best_path, 2)
                        pygame.display.update()
                        self.is_done = True
                pygame.draw.lines(self.win, BEST_LINES_COLOR,
                                      True, self.shortest_path)
                self.draw_best_distance_time()
            elif self.which_algorithm == 3 and len(self.shortest_path) > 0:
                if self.is_done == False:
                    for path in self.pos_paths:
                        for p in self.pos_paths:
                            if len(p) > 0:
                                pygame.draw.lines(self.win, ALL_LINES_COLOR, True, p)
                                pygame.display.update()
                        self.draw_ant(path)
                        self.win.blit(self.map, (585, 80))
                        self.draw_squares()
                        if self.current_distance < self.pos_best_distance:
                            self.pos_best_distance = self.current_distance
                            self.pos_best_path.clear()
                            self.pos_best_path = path
                        if len(self.pos_best_path) > 0:
                            pygame.draw.lines(self.win, BEST_LINES_COLOR,
                                True, self.pos_best_path, 2)
                        pygame.display.update()
                        self.is_done = True
                pygame.draw.lines(self.win, BEST_LINES_COLOR,
                                      True, self.shortest_path)
                self.draw_best_distance_time()
            elif self.which_algorithm == 4 and len(self.shortest_path) > 0:
                if self.is_done == False:
                    self.draw_tabu(self.pos_current)
                    self.is_done = True
                pygame.draw.lines(self.win, BEST_LINES_COLOR,
                                      True, self.shortest_path)
                self.draw_best_distance_time()
            elif self.which_algorithm == 5 and len(self.shortest_path) > 0:
                if self.is_done == False:
                    self.draw_ann(self.pos_paths)
                    self.is_done = True
                pygame.draw.lines(self.win, BEST_LINES_COLOR,
                                      True, self.shortest_path)
                self.draw_best_distance_time()
            elif self.which_algorithm == 6 and len(self.shortest_path) > 0:
                if self.is_done == False:
                    self.draw_depth(self.pos_paths)
                    self.is_done = True
                pygame.draw.lines(self.win, BEST_LINES_COLOR,
                        True, self.shortest_path)
                self.draw_best_distance_time()
            elif self.which_algorithm == 7 and len(self.shortest_path) > 0:
                if self.is_done == False:
                    self.draw_bfs(self.pos_paths)
                    self.is_done = True
                pygame.draw.lines(self.win, BEST_LINES_COLOR,
                        True, self.shortest_path)
                self.draw_best_distance_time()
            elif self.which_algorithm == 8 and len(self.shortest_path) > 0:
                if self.is_done == False:
                    self.draw_hk(self.pos_paths)
                    self.is_done = True
                pygame.draw.lines(self.win, BEST_LINES_COLOR,
                        True, self.shortest_path)
                self.draw_best_distance_time()

            pygame.display.flip()
            self.clock.tick()

    def title_display(self):
        font = pygame.font.Font(None, 36)
        text_surf = font.render(
            'Wizualizacja metrycznego problemu komiwojażera', True, DEFAULT_COLOR)
        text_width, _ = text_surf.get_size()
        x = int((WIN_WIDTH - text_width)//2)
        self.win.blit(text_surf, (x, 15))
        pygame.draw.line(self.win,
                         DEFAULT_COLOR,
                         (0, 45),
                         (WIN_WIDTH, 45),
                         width=2)

    def menu_display(self):
        ### MENU FRAME ###
        pygame.draw.polygon(self.win,
                            DEFAULT_COLOR,
                            [(10, 60), (10, 830), (350, 830), (350, 60)],
                            width=2)

        ### STATS FRAME ###
        stats_img = pygame.image.load("img/stats.png")
        resized_stats_img = pygame.transform.scale(stats_img, (40, 40))
        self.win.blit(resized_stats_img, (30, 70))

        font = pygame.font.Font(None, 40)
        stats_text = font.render('Statystyki', True, DEFAULT_COLOR)
        self.win.blit(stats_text, (85, 80))

        font = pygame.font.Font(None, 28)
        nodes = font.render(
            'Liczba wierzchołków', True, DEFAULT_COLOR)
        self.win.blit(nodes, (30, 115))
        nodes_amount = font.render(
            f'{self.slider_value}', True, DEFAULT_COLOR)
        self.win.blit(nodes_amount, (30, 135))
        best_path = font.render(
            'Najlepsza ścieżka', True, DEFAULT_COLOR)
        self.win.blit(best_path, (30, 160))
        best_path_amount = font.render(
            f'0 km', True, DEFAULT_COLOR)
        self.win.blit(best_path_amount, (30, 180))
        time_text = font.render('Czas działania', True, DEFAULT_COLOR)
        self.win.blit(time_text, (30, 200))
        time_amount = font.render(f'0 s', True, DEFAULT_COLOR)
        self.win.blit(time_amount, (30, 220))
        current_best_path = font.render(
            'Obecna ścieżka', True, DEFAULT_COLOR)
        self.win.blit(current_best_path, (30, 240))
        current_best_path_amount = font.render(
            f'0 km', True, DEFAULT_COLOR)
        self.win.blit(current_best_path_amount, (30, 260))

        ### SEPARATOR ###
        pygame.draw.line(self.win,
                         DEFAULT_COLOR,
                         (30, 290),
                         (330, 290),
                         width=2)

        ### OPTIONS FRAME ###

        options_img = pygame.image.load("img/settings.png")
        resized_options_img = pygame.transform.scale(options_img, (40, 40))
        self.win.blit(resized_options_img, (30, 295))

        font = pygame.font.Font(None, 40)
        stats_text = font.render('Opcje', True, DEFAULT_COLOR)
        self.win.blit(stats_text, (85, 310))

        self.visualization.draw(self.win)
        self.graphs.draw(self.win)

        if self.which_tab == 0:
            font = pygame.font.Font(None, 28)
            speed_of_vis_text = font.render(
            'Prędkość wizualizacji', True, DEFAULT_COLOR)
            self.win.blit(speed_of_vis_text, (30, 395))

            speed_of_vis = font.render(
            f'{self.speed[self.which_speed]}', True, DEFAULT_COLOR)
            speed_rect = speed_of_vis.get_rect(center=(180, 440))
            self.win.blit(speed_of_vis, speed_rect)

            self.left_switch_speed.draw(self.win)
            self.right_switch_speed.draw(self.win)

            node_amount = font.render(
                f'Liczba wierzchołków: {self.slider_value}', True, DEFAULT_COLOR)
            self.win.blit(node_amount, (30, 465))

            ### SLIDER VALUE ###
            pygame.draw.rect(self.win, DEFAULT_COLOR, (self.slider_x,
                            self.slider_y, self.slider_width, self.slider_height))
            slider_handle_x = int((self.slider_value - self.slider_range[0]) / (
                self.slider_range[1] - self.slider_range[0]) * self.slider_width) + self.slider_x
            slider_handle_width = 15
            pygame.draw.rect(self.win, ELEMENT_COLOR, (slider_handle_x,
                            self.slider_y, slider_handle_width, self.slider_height))

            ### POSSIBLE PATHS ###
            possible_path_text = font.render(
                'Możliwe ścieżki:', True, DEFAULT_COLOR)
            self.win.blit(possible_path_text, (30, 520))
            possible_path_amount = font.render(
                f'{self.calc_possible_paths(self.slider_value)}', True, DEFAULT_COLOR)
            self.win.blit(possible_path_amount, (30, 540))

            self.generate_nodes.draw(self.win)
            self.delete_nodes.draw(self.win)
            self.change_starting_node.draw(self.win)

            ### ALGORITHM ###
            algorithm_text = font.render('Algortym:', True, DEFAULT_COLOR)
            self.win.blit(algorithm_text, (30, 650))

            font = pygame.font.Font(None, 32)
            algorithm = font.render(
                f'{self.algorithms[self.which_algorithm]}', True, DEFAULT_COLOR)
            algorithm_rect = algorithm.get_rect(center=(180, 700))
            self.win.blit(algorithm, algorithm_rect)

            self.left_switch.draw(self.win)
            self.right_switch.draw(self.win)

            self.save_time.draw(self.win)
            self.save_distance.draw(self.win)

            if self.is_save_time == True:
                self.save_time.color = BTN_HIGHLIGHT_COLOR
            else:
                self.save_time.color = BACKGROUND_COLOR
            if self.is_save_distance == True:
                self.save_distance.color = BTN_HIGHLIGHT_COLOR
            else:
                self.save_distance.color = BACKGROUND_COLOR

            self.start.draw(self.win)

        elif self.which_tab == 1:
            ### ALGORITHM ###
            font = pygame.font.Font(None, 28)
            algorithm_text = font.render('Algortym:', True, DEFAULT_COLOR)
            self.win.blit(algorithm_text, (30, 420))

            font = pygame.font.Font(None, 32)
            algorithm = font.render(
                f'{self.algorithms[self.which_algorithm_graphs]}', True, DEFAULT_COLOR)
            algorithm_rect = algorithm.get_rect(center=(180, 480))
            self.win.blit(algorithm, algorithm_rect)

            self.left_switch_graph.draw(self.win)
            self.right_switch_graph.draw(self.win)

            self.get_time_data.draw(self.win)
            self.get_distance_data.draw(self.win)
            self.get_possible_paths_data.draw(self.win)

    def calc_possible_paths(self, value):
        result = math.factorial(int(value) - 1) / 2
        formated_result = "{:.3e}".format(result)
        if "e+0" in formated_result:
            final = formated_result.replace("e+0", "x10^")
        else:
            final = formated_result.replace("e+", "x10^")

        return final

    def switch_algorithm(self, side):
        if side == "left":
            if self.which_algorithm > 0:
                self.which_algorithm -= 1
        elif side == "right":
            if self.which_algorithm < len(self.algorithms) - 1:
                self.which_algorithm += 1
    
    def switch_algorithm_graph(self, side):
        if side == "left":
            if self.which_algorithm_graphs > 0:
                self.which_algorithm_graphs -= 1
        elif side == "right":
            if self.which_algorithm_graphs < len(self.algorithms) - 1:
                self.which_algorithm_graphs += 1

    def switch_speed(self, side):
        if side == "left":
            if self.which_speed > 0:
                self.which_speed -= 1
        elif side == "right":
            if self.which_speed < len(self.speed) - 1:
                self.which_speed += 1

    def set_speed(self):
        if self.which_speed == 0:
            speed = 25
        elif self.which_speed == 1:
            speed = 75
        elif self.which_speed == 2:
            speed = 200
        return speed

    def start_algorithm(self):
        if len(self.points_centers) > 0:
            if self.which_algorithm == 0:
                # if self.slider_value <= 10:
                    self.distance, self.work_time, self.shortest_path, self.pos_paths = brute_force(self.points_centers)   
                    self.distance *= self.pix_to_km
                    if self.is_save_time == True:    
                        self.save_time_data("brute_force", self.slider_value, self.work_time)
                    if self.is_save_distance == True:
                        self.save_dist_data("brute_force", self.slider_value, self.distance)
                        
            elif self.which_algorithm == 1:
                self.work_time, self.distance, self.shortest_path = nearest_neighbor(self.points_centers)
                self.distance *= self.pix_to_km
                if self.is_save_time == True: 
                    self.save_time_data("nearest_neighbor", self.slider_value, self.work_time)
                if self.is_save_distance == True:
                    self.save_dist_data("nearest_neighbor", self.slider_value, self.distance)

            elif self.which_algorithm == 2:
                self.work_time, self.distance, self.shortest_path, self.pos_paths = genetic_alg(self.points_centers)
                self.distance *= self.pix_to_km
                if self.is_save_time == True: 
                    self.save_time_data("genetic", self.slider_value, self.work_time)
                if self.is_save_distance == True:
                    self.save_dist_data("genetic", self.slider_value, self.distance)

            elif self.which_algorithm == 3:
                self.work_time, self.distance, self.shortest_path, self.pos_paths = ant_colony_optimization(self.points_centers)
                self.distance *= self.pix_to_km
                if self.is_save_time == True: 
                    self.save_time_data("ant", self.slider_value, self.work_time)
                if self.is_save_distance == True:
                    self.save_dist_data("ant", self.slider_value, self.distance)

            elif self.which_algorithm == 4:
                self.work_time, self.distance, self.shortest_path, self.pos_current = tabu_search(self.points_centers)
                self.distance *= self.pix_to_km 
                if self.is_save_time == True:     
                    self.save_time_data("tabu", self.slider_value, self.work_time)
                if self.is_save_distance == True:
                    self.save_dist_data("tabu", self.slider_value, self.distance)

            elif self.which_algorithm == 5:
                self.work_time, self.distance, self.shortest_path, self.pos_paths = simulated_annealing(self.points_centers)
                self.distance *= self.pix_to_km
                if self.is_save_time == True: 
                    self.save_time_data("sim_ann", self.slider_value, self.work_time)
                if self.is_save_distance == True:
                    self.save_dist_data("sim_ann", self.slider_value, self.distance)

            elif self.which_algorithm == 6:
                self.work_time, self.distance, self.shortest_path, self.pos_paths = depth_search(self.points_centers)
                self.distance *= self.pix_to_km
                if self.is_save_time == True: 
                    self.save_time_data("depth", self.slider_value, self.work_time)
                if self.is_save_distance == True:
                    self.save_dist_data("depth", self.slider_value, self.distance)

            elif self.which_algorithm == 7:
                self.work_time, self.distance, self.shortest_path, self.pos_paths = bfs(self.points_centers)
                self.distance *= self.pix_to_km
                if self.is_save_time == True: 
                    self.save_time_data("bfs", self.slider_value, self.work_time)
                if self.is_save_distance == True:
                    self.save_dist_data("bfs", self.slider_value, self.distance)

            elif self.which_algorithm == 8:
                self.work_time, self.distance, self.shortest_path, self.pos_paths = held_karp(self.points_centers)
                self.distance *= self.pix_to_km
                if self.is_save_time == True: 
                    self.save_time_data("held_karp", self.slider_value, self.work_time)
                if self.is_save_distance == True:
                    self.save_dist_data("held_karp", self.slider_value, self.distance)

    def switch_starting_node(self, points):
        indeks = random.randint(1, len(points) - 1)
        points[0], points[indeks] = points[indeks], points[0]
        return points

    def popup_window(self, surface, x, y, text):
        lines = text.split("\n")
        line_height = 20
        bg_popup = pygame.Surface((x+10, y+10))
        bg_popup.fill(DEFAULT_COLOR)
        popup = pygame.Surface((x, y))
        popup.fill(BACKGROUND_COLOR)
        font = pygame.font.Font(None, 22)
        for line in lines:
            temp_text = font.render(line, True, DEFAULT_COLOR)
            popup.blit(temp_text, ((popup.get_width() - temp_text.get_width()) // 2, line_height))
            line_height += font.get_linesize()

        bg_popup.blit(popup, (5, 5))
        surface.blit(bg_popup, ((WIN_WIDTH//2-(x+10)//2), (WIN_HEIGHT//2)-(y+10)//2))

    def save_time_data(self, name, nodes_amount, time):
        temp_dict = {
            "alg_name": name,
            "nodes_amount": nodes_amount,
            "time": time
        }

        update_json_data("data/time_data.json", temp_dict)

    def save_dist_data(self, name, nodes_amount, distance):
        temp_dict = {
            "alg_name": name,
            "nodes_amount": nodes_amount,
            "distance": distance
        }

        update_json_data("data/distance_data.json", temp_dict)

    def switch_boolean_time(self):
        if self.is_save_time == False:
            self.is_save_time = True
        else:
            self.is_save_time = False

    def switch_boolean_dist(self):
        if self.is_save_distance == False:
            self.is_save_distance = True
        else:
            self.is_save_distance = False

    def chosen_points(self, amount):
        temp_list = []

        for i in range(0, amount):
            temp_list.append(nodes100[i])

        return temp_list

    def draw_squares(self):
        for point in self.points:
            if self.points.index(point) == 0:
                pygame.draw.rect(
                    self.win, STARTING_POINT_COLOR, (point[0], point[1], 10, 10))
            else:
                pygame.draw.rect(
                    self.win, OTHER_POINT_COLOR, (point[0], point[1], 10, 10))

    def draw_best_distance_time(self):
        font = pygame.font.Font(None, 28)
        best_path = font.render(
            'Najlepsza ścieżka', True, DEFAULT_COLOR)
        self.win.blit(best_path, (30, 160))
        best_path_amount = font.render(
            f'{round(self.distance, 3)} km', True, DEFAULT_COLOR)
        self.win.blit(best_path_amount, (30, 180))
        time_text = font.render('Czas działania', True, DEFAULT_COLOR)
        self.win.blit(time_text, (30, 200))
        time_amount = font.render(f'{round(self.work_time, 8)} s', True, DEFAULT_COLOR)
        self.win.blit(time_amount, (30, 220))
        pygame.draw.rect(self.win, BACKGROUND_COLOR, (30, 160, 180, 80))
        self.win.blit(best_path, (30, 160))
        self.win.blit(best_path_amount, (30, 180))
        self.win.blit(time_text, (30, 200))
        self.win.blit(time_amount, (30, 220))
        pygame.display.update()

    def draw_current_distance(self):
        font = pygame.font.Font(None, 28)
        current_best_path = font.render(
            'Obecna ścieżka', True, DEFAULT_COLOR)
        self.win.blit(current_best_path, (30, 240))
        current_best_path_amount = font.render(
            f'{round(self.current_distance, 3)} km', True, DEFAULT_COLOR)
        self.win.blit(current_best_path_amount, (30, 260))
        pygame.draw.rect(self.win, BACKGROUND_COLOR, (30, 240, 150, 50))
        self.win.blit(current_best_path, (30, 240))
        self.win.blit(current_best_path_amount, (30, 260))
        pygame.display.update()

    def draw_bf(self, path):
        speed = self.set_speed()

        self.current_distance = 0
        pygame.time.delay(50)
        for i in range(len(path)-1):            
            pygame.draw.line(self.win, ALL_LINES_COLOR, path[i], path[i+1])
            self.current_distance += math.sqrt((path[i][0]-path[i+1][0])
                                  ** 2 + (path[i][1]-path[i+1][1])**2)
            pygame.display.update()
            self.draw_current_distance()            
            pygame.time.delay(speed)
        pygame.draw.line(self.win, ALL_LINES_COLOR, path[-i], path[0])
        pygame.display.update()
        self.current_distance *= self.pix_to_km
        self.draw_current_distance()
        pygame.time.delay(500)
    
    def draw_nn(self, path):
        speed = self.set_speed()
        l = []

        self.current_distance = 0
        pygame.time.delay(50)
        for i in range(len(path)-1):
            pygame.draw.line(self.win, ALL_LINES_COLOR, path[i], path[i+1])
            self.current_distance += math.sqrt((path[i][0]-path[i+1][0])
                                ** 2 + (path[i][1]-path[i+1][1])**2)
            pygame.display.update()
            self.draw_current_distance() 
            pygame.time.delay(speed)

            # Rysowanie linii między obecnym punktem a pozostałymi w kolorze czarnym
            for j in range(i+1, len(path)):
                pygame.draw.line(self.win, ALL_LINES_COLOR, path[i], path[j])
                pygame.display.update()
                pygame.time.delay(speed)


            # Rysowanie najkrótszej linii w kolorze niebieskim
            shortest_distance = float('inf')
            shortest_index = 0
            for j in range(i+1, len(path)):
                distance = math.sqrt((path[i][0]-path[j][0])**2 + (path[i][1]-path[j][1])**2)
                if distance < shortest_distance:
                    shortest_distance = distance
                    shortest_index = j
            pygame.time.delay(500)
            pygame.draw.line(self.win, STARTING_POINT_COLOR, path[i], path[shortest_index], 3)
            l.append((path[i], path[shortest_index]))
            pygame.display.update()
            pygame.time.delay(500)
            self.win.blit(self.map, (585, 80))
            self.draw_squares()
            pygame.draw.line(self.win, STARTING_POINT_COLOR, l[0][0], l[0][1], 3)
            for line in range(len(l)-1):
                pygame.draw.lines(self.win, STARTING_POINT_COLOR, l[line], l[line+1], 3)

        # Rysowanie linii między ostatnim punktem a pierwszym w kolorze czarnym
        pygame.draw.line(self.win, STARTING_POINT_COLOR, path[-1], path[0], 3)
        pygame.display.update()
        self.current_distance += math.sqrt((path[-1][0]-path[0][0])
                        ** 2 + (path[-1][1]-path[0][1])**2)
        self.current_distance *= self.pix_to_km
        self.draw_current_distance()
        pygame.time.delay(500)

    def draw_gen(self, path):
        speed = self.set_speed()

        self.current_distance = 0
        pygame.time.delay(50)
        for i in range(len(path)-1):            
            pygame.draw.line(self.win, ALL_LINES_COLOR, path[i], path[i+1])
            self.current_distance += math.sqrt((path[i][0]-path[i+1][0])
                                  ** 2 + (path[i][1]-path[i+1][1])**2)
            pygame.display.update()
            self.draw_current_distance()       
            pygame.time.delay(speed)
        pygame.draw.line(self.win, ALL_LINES_COLOR, path[-1], path[0])
        pygame.display.update()
        self.current_distance += math.sqrt((path[-1][0]-path[0][0])
                        ** 2 + (path[-1][1]-path[0][1])**2)
        self.current_distance *= self.pix_to_km
        self.draw_current_distance()
        pygame.time.delay(500)

    def draw_ant(self, path):
        speed = self.set_speed()

        self.current_distance = 0
        pygame.time.delay(50)
        for i in range(len(path)-1):            
            pygame.draw.line(self.win, ALL_LINES_COLOR, path[i], path[i+1])
            self.current_distance += math.sqrt((path[i][0]-path[i+1][0])
                                  ** 2 + (path[i][1]-path[i+1][1])**2)
            pygame.display.update()
            self.draw_current_distance()       
            pygame.time.delay(speed)
        pygame.draw.line(self.win, ALL_LINES_COLOR, path[-1], path[0])
        pygame.display.update()
        self.current_distance += math.sqrt((path[-1][0]-path[0][0])
                        ** 2 + (path[-1][1]-path[0][1])**2)
        self.current_distance *= self.pix_to_km
        self.draw_current_distance()
        pygame.time.delay(500)
            
    def draw_tabu(self, current_path):
        speed = self.set_speed()

        self.current_distance = 0
        pygame.time.delay(50)
        random.shuffle(current_path)
        
        for num in range(len(current_path)):
            for i in range(len(current_path[num])-1):
                current = current_path[num][i]
                next_ = current_path[num][i+1]
                pygame.draw.line(self.win, ALL_LINES_COLOR, current, next_)
                pygame.display.update()
                pygame.time.delay(speed)
            
            last = current_path[num][-1]
            starting = current_path[num][0]
            pygame.draw.line(self.win, ALL_LINES_COLOR, last, starting)
            pygame.display.update()
            pygame.time.delay(speed)
            
            self.current_distance = 0
            for i in range(len(current_path[num])-1):
                current = current_path[num][i]
                next_ = current_path[num][i+1]
                self.current_distance += math.sqrt((current[0]-next_[0])**2 + (current[1]-next_[1])**2)
            
            self.current_distance += math.sqrt((last[0]-starting[0])**2 + (last[1]-starting[1])**2)
            self.current_distance *= self.pix_to_km
            
            self.draw_current_distance() 
            
            pygame.time.delay(500)
            self.win.blit(self.map, (585, 80))
            self.draw_squares()
            pygame.display.update()

            if self.current_distance < self.pos_best_distance:
                self.pos_best_distance = self.current_distance
                pygame.draw.polygon(self.win, BEST_LINES_COLOR, current_path[num], 2)
                pygame.display.update()
                pygame.time.delay(speed)

    def draw_ann(self, path):
        speed = self.set_speed()
        dist_list = []

        if len(path) > 1:
            pygame.time.delay(speed)
            for _ in range(len(path)):
                
                for i in path:
                    pygame.draw.polygon(self.win, ALL_LINES_COLOR, i, 1)
                    self.current_distance = 0
                    for j in range(len(i)-1):
                        self.current_distance += math.sqrt((i[j][0]-i[j+1][0])**2 + (i[j][1]-i[j+1][1])**2) * self.pix_to_km
                    self.current_distance += math.sqrt((i[-1][0]-i[0][0])**2 + (i[-1][1]-i[-1][1])**2) * self.pix_to_km 
                # self.draw_current_distance()
                pygame.display.update()
                pygame.time.delay(speed)

                    
                dist_list.append(self.current_distance)                                               

                idx_longes_dist = dist_list.index(max(dist_list))

                path.pop(idx_longes_dist)

                dist_list.pop(idx_longes_dist)

                self.win.blit(self.map, (585, 80))
                self.draw_squares()
                pygame.display.update()
                print(len(path))

    def draw_depth(self, path):
        speed = self.set_speed()
        tsp_path = []
        for p in path:
            tsp_path.extend(p)
            tsp_path.append(p[0])

        for i in range(len(tsp_path)-1):
            pygame.draw.line(self.win, ALL_LINES_COLOR, tsp_path[i], tsp_path[i+1])
            self.current_distance += math.sqrt((tsp_path[i][0]-tsp_path[i+1][0])**2 + (tsp_path[i][1]-tsp_path[i+1][1])**2) * self.pix_to_km
            self.draw_current_distance()
            pygame.display.update()
            pygame.time.delay(speed)
            self.win.blit(self.map, (585, 80))
            self.draw_squares()
            pygame.display.update()

    def draw_bfs(self, path):
        speed = self.set_speed()
        for p in path:
            self.current_distance = 0
            pygame.draw.polygon(self.win, ALL_LINES_COLOR, p, 1)
            for j in range(len(p)-1):
                self.current_distance += math.sqrt((p[j][0]-p[j+1][0])**2 + (p[j][1]-p[j+1][1])**2) * self.pix_to_km
            self.current_distance += math.sqrt((p[-1][0]-p[0][0])**2 + (p[-1][1]-p[0][1])**2) * self.pix_to_km
            pygame.display.update()
            pygame.time.delay(speed)
            self.win.blit(self.map, (585, 80))
            self.draw_squares()
            pygame.display.update()
            self.draw_current_distance()

    def draw_hk(self, path):
        for p in path:
            self.current_distance = 0
            for i in range(len(p)-1):
                pygame.draw.line(self.win, ALL_LINES_COLOR, p[i], p[i+1])
                pygame.display.update()
                pygame.time.delay(100)
                self.current_distance += math.sqrt((p[i][0]-p[i+1][0])**2 + (p[i][1]-p[i+1][1])**2) * self.pix_to_km
                self.current_distance += math.sqrt((p[-1][0]-p[0][0])**2 + (p[-1][1]-p[0][1])**2) * self.pix_to_km
            self.draw_current_distance()
            self.win.blit(self.map, (585, 80))
            self.draw_squares()
            pygame.display.update()

class Button:
    def __init__(self, x, y, width, height, text_lines, font_size=24, text_color=ELEMENT_COLOR, color=BACKGROUND_COLOR, border_color=DEFAULT_COLOR, border_width=2):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_lines = text_lines
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.border_rect = self.rect.inflate(
            self.border_width*2, self.border_width*2)

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.border_rect)
        pygame.draw.rect(surface, self.color, self.rect)
        line_height = self.font.get_linesize()
        y = self.rect.centery - line_height * (len(self.text_lines) / 2)
        for line in self.text_lines:
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(
                center=(self.rect.centerx, y + 10))
            surface.blit(text_surface, text_rect)
            y += line_height

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False
