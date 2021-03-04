#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 最短路径/SP
@file_name: SP.py
@project: Algorithm
@version: 1.0
@date: 2021/03/03 18:47
@author: Air
"""

__author__ = 'Air'

from collections import defaultdict
import heapq
from math import log
from typing import List


class Graph:
    def __init__(self, vertices: int) -> None:
        """
        初始化图
        :param vertices: 顶点数
        """
        self.graph = defaultdict(defaultdict)
        self.V = vertices
        self.path = [-1] * vertices
        self.order = []
        self.q = [False] * vertices
        self.edges = []
        self.cycle = []

    def add_edge(self, v: int, w: int, weight: float = 0.0) -> None:
        """
        增加加权边
        :param v: 起点
        :param w: 终点
        :param weight: 权重
        :return:
        """
        self.graph[v][w] = weight
        self.edges.append((v, w, weight))

    def topological_sort_util(self, v: int, visited: List[bool]) -> None:
        """
        拓扑排序工具函数
        :param v: 当前顶点
        :param visited: 记录是否访问
        :return:
        """
        visited[v] = True
        for w in self.graph[v]:
            if not visited[w]:
                self.topological_sort_util(w, visited)
        self.order.insert(0, v)

    def topological_sort(self) -> None:
        """
        拓扑排序
        :return:
        """
        visited = [False] * self.V
        for v in range(self.V):
            if not visited[v]:
                self.topological_sort_util(v, visited)

    def dijkstra(self, starting_vertex: int) -> dict:
        """
        Dijkstra算法求最短路径
        :param starting_vertex: 初始顶点
        :return: 由初始顶点到各顶点的最短距离
        """
        distances = {vertex: float('inf') for vertex in range(self.V)}
        distances[starting_vertex] = 0.0
        pq = [(0, starting_vertex)]
        while pq:
            current_distance, current_vertex = heapq.heappop(pq)
            if current_distance > distances[current_vertex]:
                continue
            for neighbor, weight in self.graph[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    self.path[neighbor] = current_vertex
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        return distances

    def acyclic_sp(self, starting_vertex: int) -> dict:
        """
        无环加权有向图中的最短路径算法
        :param starting_vertex:
        :return:
        """
        distances = {vertex: float('inf') for vertex in range(self.V)}
        distances[starting_vertex] = 0.0
        self.topological_sort()
        for current_vertex in self.order:
            for neighbor, weight in self.graph[current_vertex].items():
                distance = distances[current_vertex] + weight
                if distance < distances[neighbor]:
                    self.path[neighbor] = current_vertex
                    distances[neighbor] = distance
        return distances

    def acyclic_lp(self, starting_vertex: int) -> dict:
        """
        无环加权有向图中的最长路径算法
        :param starting_vertex: 起点
        :return:
        """
        distances = {vertex: -float('inf') for vertex in range(self.V)}
        distances[starting_vertex] = 0.0
        self.topological_sort()
        for current_vertex in self.order:
            for neighbor, weight in self.graph[current_vertex].items():
                distance = distances[current_vertex] + weight
                if distance > distances[neighbor]:
                    self.path[neighbor] = current_vertex
                    distances[neighbor] = distance
        return distances

    def bellman_ford_sp(self, starting_vertex: int) -> dict:
        distances = {vertex: float('inf') for vertex in range(self.V)}
        queue = [starting_vertex]
        distances[starting_vertex] = 0.0
        self.q[starting_vertex] = True
        cost = 0
        change = False

        def has_negative_cycle() -> bool:
            """
            查找是否有负环
            :return: 是否有负环
            """
            for edge in self.edges:
                if distances[edge[0]] != float('inf') and distances[edge[1]] + edge[2] < distances[edge[0]]:
                    return True
            return False

        def find_negative_cycle() -> List[int]:
            """
            找到一个负环
            :return: 负环上的节点
            """
            visited = [False] * self.V
            now = [False] * self.V
            edge_to = [-1] * self.V
            cycle = []

            def dfs(cur: int) -> None:
                """
                深度优先遍历图
                :param cur: 当前节点
                :return:
                """
                now[cur] = True
                visited[cur] = True
                for nei, _ in self.graph[cur].items():
                    if cycle:
                        return
                    elif not visited[nei]:
                        edge_to[nei] = cur
                        dfs(nei)
                    elif now[nei]:
                        x = cur
                        while x != nei:
                            cycle.append(x)
                            x = edge_to[x]
                        cycle.append(nei)
                        cycle.append(cur)
                now[cur] = False

            for vertex in range(self.V):
                if not visited[vertex] and not cycle:
                    dfs(v)
            return cycle

        while queue:
            v = queue.pop(0)
            self.q[v] = False
            for neighbor, weight in self.graph[v].items():
                distance = distances[v] + weight
                if distance < distances[neighbor]:
                    self.path[neighbor] = v
                    distances[neighbor] = distance
                    if not self.q[neighbor]:
                        queue.append(neighbor)
                        self.q[neighbor] = True
                    change = True
            cost += 1
            if not change:
                break
            if cost % self.V == 0 and has_negative_cycle():
                self.cycle = find_negative_cycle()
                break
        return distances


if __name__ == '__main__':
    def input_data(file_name: str) -> Graph:
        with open(file_name, 'r', encoding='utf-8') as fl:
            lines = fl.readlines()
        graph = Graph(int(lines[0]))
        for i in range(2, len(lines)):
            line = lines[i].strip().split(" ")
            graph.add_edge(int(line[0]), int(line[1]), float(line[2]))
        return graph

    # dijkstra
    g = input_data('tinyEWD.txt')
    print(g.dijkstra(0))
    print(g.path)

    # acyclic_sp
    g = input_data('tinyEWDAG.txt')
    print(g.acyclic_sp(5))
    print(g.path)

    # acyclic_lp
    print(g.acyclic_lp(5))
    print(g.path)

    # topological_sort
    g = Graph(6)
    g.add_edge(5, 2)
    g.add_edge(5, 0)
    g.add_edge(4, 0)
    g.add_edge(4, 1)
    g.add_edge(2, 3)
    g.add_edge(3, 1)
    g.topological_sort()
    print(g.order)

    # CPM/并行调度任务/关键路径
    with open('josPC.txt', 'r', encoding='utf-8') as f:
        ls = f.readlines()
        n = int(ls[0])
        s = n << 1
        t = s + 1
        g = Graph(t + 1)
        j = 0
        for m in range(1, len(ls)):
            ln = ls[m].strip().split(" ")
            duration = float(ln[0])
            g.add_edge(j, j + n, duration)
            g.add_edge(s, j)
            g.add_edge(j + n, t)
            for k in range(1, len(ln)):
                g.add_edge(j + n, int(ln[k]))
            j += 1
    print("Start times:")
    d = g.acyclic_lp(s)
    for k in range(10):
        print(str(k) + ": " + str(d[k]))
    print("Finish time:")
    print(d[t])

    # bellman_ford_sp
    g = input_data('tinyEWDn.txt')
    print(g.bellman_ford_sp(0))
    print(g.path)

    # bellman_ford_sp with negative cycle
    g = input_data('tinyEWDnc.txt')
    print(g.bellman_ford_sp(0))
    print(g.path)
    print(g.cycle)
