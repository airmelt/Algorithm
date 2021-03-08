#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 树状数组/BIT
@file_name: BIT.py
@project: Algorithm
@version: 1.0
@date: 2021/3/8 23:30
@author: airmelt
"""


class BIT:
    def __init__(self, n: int) -> None:
        """
        初始化树状数组
        :param n: 树状数组容量
        """
        self.n = n
        self.tree = [0] * (n + 1)

    def lowbit(self, x: int) -> int:
        """
        得到一个数的最低位对应的 2的幂
        如 2(0b10) -> 2, 7(0b111) -> 1
        :param x: 输入一个整数
        :return: 得到其最低位对应的 2的幂
        """
        return x & (-x)

    def update(self, x: int, k: int) -> None:
        """
        单点更新 给 a[x] + k
        :param x: 下标
        :param k: 更新值
        :return:
        """
        while x <= self.n:
            self.tree[x] += k
            x += self.lowbit(x)

    def query(self, x: int) -> int:
        """
        区间查询 sum(a[:x + 1])
        :param x: 查询下标
        :return:
        """
        result = 0
        while x:
            result += self.tree[x]
            x -= self.lowbit(x)
        return result
