#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 扩展欧几里德/gcd
@file_name: GCD.py
@project: Algorithm
@version: 1.0
@date: 2021/12/18 16:57
@author: airmelt
"""


def ex_gcd(a: int, b: int) -> tuple:
    """
    扩展欧几里德算法是用来在已知 a, b 求解一组 p，q 使得 p * a + q * b = Gcd(a, b)
    :param a:
    :param b:
    :return:
    """
    if b == 0:
        return a, 1, 0
    d, x, y = ex_gcd(b, a % b)
    p, q = y, x - (a // b) * y
    return d, p, q
