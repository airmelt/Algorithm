#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 差分数组/Array of Difference
@file_name: Diff.py
@project: Algorithm
@version: 1.0
@date: 2021/11/12 20:25
@author: airmelt
"""

from typing import List


class Diff:
    def __init__(self, arr: List[int]) -> None:
        self.diff = [arr[0]] * len(arr)
        for i in range(1, len(arr)):
            self.diff[i] = arr[i] - arr[i - 1]

    def modify(self, i: int, j: int, value: int) -> None:
        """
        取 [i, j] 双闭区间进行区间修改
        对区间修改只需要 diff[i] += value, diff[j + 1] -= value
        :param i: 起点
        :param j: 终点
        :param value: 修改值
        :return:
        """
        self.diff[i] += value
        if j + 1 < len(self.diff):
            self.diff[j + 1] -= value

    def recover(self) -> List[int]:
        """
        复原数组
        :return: 原数组
        """
        result = [self.diff[0]]
        for i in range(1, len(self.diff)):
            result.append(result[-1] + self.diff[i])
        return result
