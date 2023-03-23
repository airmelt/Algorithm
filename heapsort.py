#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: heapsort
@file_name: heapsort.py
@project: Algorithm
@version: 1.0
@date: 2023/3/5 14:21
@author: air
"""
from typing import NoReturn, List, Optional


def heapify(arr: List[Optional], n: int, i: int) -> NoReturn:
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[largest] < arr[left]:
        largest = left
    if right < n and arr[largest] < arr[right]:
        largest = right
    if i != largest:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heapsort(arr: List[Optional]) -> NoReturn:
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
