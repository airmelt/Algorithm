#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: convex hull/凸包
@file_name: convex_hull.py
@project: Algorithm
@version: 1.0
@date: 2021/4/25 21:26
@author: airmelt
"""


def convex_hull(trees: list) -> list:
    """
    返回一个数组的凸包
    :param trees: 定义 trees 中有 n 个点 [x0, y0], [x1, y1], ..., [xn, yn]
    :return: 一个凸包的集
    """
    n = len(trees)
    if n < 3:
        return trees
    trees.sort(key=lambda x: (x[0], x[1]))
    cross, low, up = lambda a, b, c: (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]), [], []
    for p in trees:
        while len(low) > 1 and cross(low[-2], low[-1], p) < 0:
            low.pop()
        low.append((p[0], p[1]))
    for p in reversed(trees):
        while len(up) > 1 and cross(up[-2], up[-1], p) < 0:
            up.pop()
        up.append((p[0], p[1]))
    return list(set(low[:-1] + up[:-1]))
