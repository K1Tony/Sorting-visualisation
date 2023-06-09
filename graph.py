import math
import random
import constants as cs
import queue as q
import time
import pygame as pg


class Arrow:
    def __init__(self, start: tuple, end: tuple, angle: float, width: int = 2):
        self.start = start
        self.end = end
        self.angle = angle
        self.width = width
        self.edges = [(end, (end[0] + cs.ARROW * math.cos(self.angle + math.pi * 0.25),
                             end[1] + cs.ARROW * math.sin(self.angle + math.pi * 0.25))),
                      (end, (end[0] + cs.ARROW * math.cos(self.angle - math.pi * 0.25),
                             end[1] + cs.ARROW * math.sin(self.angle - math.pi * 0.25)))]


class Graph:
    def __init__(self, size: int, directed=False, weighted=False,
                 negative=False, connected=True):
        self.size = size
        self.directed = directed
        self.weighted = weighted
        self.negative = negative
        self.connected = connected

        self.matrix = False
        self.graph_list = [[] for _ in range(self.size)]
        self.graph_matrix = [[math.inf if self.weighted else False for _ in range(self.size)]
                             for _ in range(self.size)]
        self.edges = random.randint(0, self.size - 2) if not connected else \
            random.randint(self.size - 1, self.size * (self.size - 1) // 2)

        self.visited = [False] * self.size
        self.parent = [None] * self.size
        self.edge_visited = {}
        self.graph_nodes = []
        self.edge_list = []
        self.times = [-1] * self.size

    def create(self):
        edges = self.edges
        self.graph_list = [[] for _ in range(self.size)]
        self.graph_matrix = [[math.inf if self.weighted else False for _ in range(self.size)]
                             for _ in range(self.size)]
        if self.connected:
            visited = [False] * self.size
            v = 0
            visited[v] = True
            for _ in range(self.size - 1):
                available = [i for i in range(self.size) if not visited[i]]
                u = random.choice(available)
                visited[u] = True
                if self.weighted:
                    if self.negative:
                        w = random.randint(-cs.WEIGHT_BOUND, cs.WEIGHT_BOUND)
                    else:
                        w = random.randint(0, cs.WEIGHT_BOUND)
                    self.graph_matrix[v][u] = w
                    self.graph_list[v].append((u, w))
                    if not self.directed:
                        self.graph_matrix[u][v] = w
                        self.graph_list[u].append((v, w))
                else:
                    self.graph_matrix[v][u] = True
                    self.graph_list[v].append(u)
                    if not self.directed:
                        self.graph_matrix[u][v] = True
                        self.graph_list[u].append(v)
                v = u
            edges -= self.size - 1

        for _ in range(edges):
            first = [i for i in range(self.size) if len(self.graph_list[i]) < self.size - 1]
            if not first: break
            v = random.choice(first)
            second = [i for i in range(self.size) if
                      (self.weighted and not math.isinf(self.graph_matrix[v][i]) and
                       not math.isinf(self.graph_matrix[i][v])) or (
                              not self.weighted and not self.graph_matrix[v][i] and not
                      self.graph_matrix[i][v]
                      )]
            if not second: break
            u = random.choice(second)
            if self.weighted:
                if self.negative:
                    w = random.randint(-cs.WEIGHT_BOUND, cs.WEIGHT_BOUND)
                else:
                    w = random.randint(0, cs.WEIGHT_BOUND)
                self.graph_list[v].append((u, w))
                self.graph_matrix[v][u] = w
                if not self.directed:
                    self.graph_matrix[u][v] = w
                    self.graph_list[u].append((v, w))
            else:
                self.graph_matrix[v][u] = True
                self.graph_list[v].append(u)
                if not self.directed:
                    self.graph_matrix[u][v] = True
                    self.graph_list[u].append(v)

        center = (cs.WIDTH // 2, cs.HEIGHT // 2)
        ang = 2 * math.pi / self.size
        distance = cs.HEIGHT // 2

        self.graph_nodes.clear()
        for i in range(self.size):
            self.graph_nodes.append(pg.Rect(center[0] - distance * math.cos(ang * i) - cs.SIZE // 2,
                                            center[1] - distance * math.sin(ang * i) - cs.SIZE // 2,
                                            cs.SIZE, cs.SIZE))
        self.edge_list.clear()
        self.set_edges()

    def set_edges(self):
        for i in range(self.size):
            for j in self.graph_list[i]:
                line = self.graph_nodes[i].center, self.graph_nodes[j].center
                if self.directed:
                    if self.graph_nodes[i].x == self.graph_nodes[j].x:
                        if self.graph_nodes[i].y > self.graph_nodes[j].y: angle = math.pi / 2
                        else: angle = math.pi * 1.5
                    else:
                        angle = math.pi / 2 if self.graph_nodes[i].x == self.graph_nodes[j].x else\
                            math.atan((self.graph_nodes[j].y - self.graph_nodes[i].y) / (self.graph_nodes[j].x -
                                                                                         self.graph_nodes[i].x))
                        if self.graph_nodes[i].x < self.graph_nodes[j].x: angle += math.pi
                    edge = Arrow(line[0], line[1], angle)
                    self.edge_list.append(edge)
                else:
                    line = self.graph_nodes[i].center, self.graph_nodes[j].center
                    self.edge_list.append(line)
                self.edge_visited[line] = 0

    def bfs(self, s=0):
        dst = [math.inf] * self.size
        self.visited[s] = True
        dst[s] = 0
        Q = q.Queue()
        Q.put(s)

        while not Q.empty():
            u = Q.get()
            for v in self.graph_list[u]:
                if self.weighted: v = v[0]
                if not self.visited[v]:
                    self.visited[v] = True
                    self.edge_visited[(self.graph_nodes[v].center, self.graph_nodes[u].center)] = 1
                    self.edge_visited[(self.graph_nodes[u].center, self.graph_nodes[v].center)] = 1
                    dst[v] = dst[u] + 1
                    self.parent[v] = u
                    Q.put(v)
                    time.sleep(0.3)

    def dfs(self, s=0):
        max_time = 0

        def visit(v):
            nonlocal max_time
            self.visited[v] = True
            max_time += 1
            self.times[v] = max_time
            time.sleep(0.3)
            for u in self.graph_list[v]:
                if self.weighted: u = u[0]
                if not self.visited[u]:
                    self.parent[u] = v
                    self.edge_visited[(self.graph_nodes[v].center, self.graph_nodes[u].center)] = 1
                    self.edge_visited[(self.graph_nodes[u].center, self.graph_nodes[v].center)] = 1
                    visit(u)

        visit(s)

    def is_bipartite(self):
        pass

    def is_connected(self):
        pass

    def topological_sort(self):
        pass

    def euler_cycle(self):
        pass

    def find_strong_components(self):
        pass

    def find_bridges(self):
        pass

    def shortest_path(self):
        if not self.weighted: self.bfs()

    def shortest_path_negative(self):
        pass

    def all_shortest_paths(self):
        pass

    def find_mst(self):
        pass

    def max_flow(self):
        pass
