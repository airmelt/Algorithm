#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 全排列/permutation
@file_name: permutation.py
@project: Algorithm
@version: 1.0
@date: 2019/04/30 16:04
@author: air
"""

__author__ = 'air'


def permutation(array: list, position: int=0, end: int=100) -> None:
    """
    普通递归实现全排列, 基于交换
    :param array: 需要全排列的列表
    :param position: 开始位置
    :param end: 结束位置
    :return:
    """
    if end > len(array):
        end = len(array)
    if position == end:
        print(array)
    else:
        for index in range(position, end):
            array[index], array[position] = array[position], array[index]
            permutation(array, position + 1, end)
            array[index], array[position] = array[position], array[index]


def dfs_permutation(array: list, position: int=0) -> None:
    """
    深度优先搜索实现全排列
    :param array: 需要全排列的列表
    :param position: 位置参数, 记录递归终点
    :return:
    """
    visit = [True] * len(array)
    temp = [''] * len(array)

    def dfs(pos):
        if pos == len(array):
            print(temp)
            return
        for index in range(0, len(array)):
            if visit[index]:
                temp[pos] = array[index]
                visit[index] = False
                dfs(pos + 1)
                visit[index] = True
    dfs(position)


if __name__ == '__main__':
    arr = ['a', 'b', 'c']
    # permutation(arr)
    dfs_permutation(arr)
