#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 最小生成树/MST
@file_name: MST.py
@project: Algorithm
@version: 1.0
@date: 2021/03/03 15:31
@author: Air
"""

__author__ = 'Air'

import collections
from queue import PriorityQueue

from typing import List

from UF import UF


class Edge:
    def __init__(self, v: int, w: int, weight: float) -> None:
        """
        带权边
        :param v: 一个顶点
        :param w: 另一个顶点
        :param weight: 权重
        :return:
        """
        self.v = v
        self.w = w
        self.weight = weight

    def __lt__(self, other) -> None:
        """
        自定义比较函数
        :param other:
        :return:
        """
        return other.weight > self.weight

    def __str__(self):
        return str(self.v) + " - " + str(self.w) + " " + str(self.weight)


class EdgeWeightedGraph:
    def __init__(self, v: int) -> None:
        """
        加权无向图
        :param v: 顶点数
        :return:
        """
        self.V = v
        self.E = 0
        self.adj = collections.defaultdict(list)

    def add_edge(self, e: Edge) -> None:
        """
        增加一条边
        :param e: 边
        :return:
        """
        self.adj[e.v].append(Edge(e.v, e.w, e.weight))
        self.adj[e.w].append(Edge(e.w, e.v, e.weight))
        self.E += 1

    def edges(self) -> List[Edge]:
        """
        返回加权无向图中的所有边
        :return: 边的列表
        """
        result = []
        for v in range(self.V):
            for e in self.adj[v]:
                if e.w > v:
                    result.append(e)
        return result


class LazyPrimMST:
    def __init__(self, g: EdgeWeightedGraph) -> None:
        """
        初始化延时 Prim算法类
        :param g: 加权无向图
        """
        self.pq = PriorityQueue()
        self.marked = [False] * g.V
        self.mst = []
        self.visit(g, 0)
        while not self.pq.empty():
            e = self.pq.get()
            v = e.v
            w = e.w
            if self.marked[v] and self.marked[w]:
                continue
            self.mst.append(e)
            if not self.marked[v]:
                self.visit(g, v)
            if not self.marked[w]:
                self.visit(g, w)

    def visit(self, g: EdgeWeightedGraph, v: int) -> None:
        """
        访问 v的所有邻边
        :param g: 加权无向图
        :param v: 访问顶点
        :return:
        """
        self.marked[v] = True
        for e in g.adj[v]:
            if not self.marked[e.w]:
                self.pq.put(e)

    def edges(self) -> List[Edge]:
        """
        返回最小生成树
        :return: 最小生成树
        """
        return self.mst

    def weight(self) -> float:
        """
        计算最小生成树的权重和
        :return: 最小生成树的权重和
        """
        return sum(e.weight for e in self.mst)


class KruskalMST:
    def __init__(self, g: EdgeWeightedGraph) -> None:
        self.mst = []
        self.pq = PriorityQueue()
        for e in g.edges():
            self.pq.put(e)
        uf = UF(g.V)
        while not self.pq.empty() and len(self.mst) < g.V - 1:
            e = self.pq.get()
            v = e.v
            w = e.w
            if uf.connected(v, w):
                continue
            uf.union(v, w)
            self.mst.append(e)

    def edges(self) -> List[Edge]:
        return self.mst

    def weight(self) -> float:
        return sum(e.weight for e in self.mst)


if __name__ == '__main__':
    with open('tinyEWG.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        line = lines[0].strip().split(" ")
        graph = EdgeWeightedGraph(int(line[0]))
    for i in range(1, len(lines)):
        line = lines[i].strip().split(" ")
        graph.add_edge(Edge(int(line[0]), int(line[1]), float(line[2])))
    prim = LazyPrimMST(graph)
    print("-----PrimMST-----")
    print([str(edge) for edge in prim.edges()])
    print("---PrimWeight----")
    print(prim.weight())
    kruskal = KruskalMST(graph)
    print("---KruskalMST----")
    print([str(edge) for edge in kruskal.edges()])
    print("--KruskalWeight--")
    print(kruskal.weight())
