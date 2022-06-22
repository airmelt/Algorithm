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
from typing import List


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


def matrix_ex_gcd(a: int, b: int) -> tuple:
    """
    矩阵迭代方式求扩展欧几里得算法
    :param a:
    :param b:
    :return:
    """
    x1, x2, x3, x4 = 1, 0, 0, 1
    while b:
        c = a // b
        x1, x2, x3, x4, a, b = x3, x4, x1 - x3 * c, x2 - x4 * c, b, a - b * c
    return a, x1, x2


def inverse(n: int, p: int) -> List[int]:
    """
    线性法求逆元
    逆元 ax = 1(mod b) -> x = a ^ (b - 2)(mod b)
    :param n: 范围
    :param p: mod, 一般为 10 ** 9 + 7
    :return:
    """
    inv = list(range(1, n + 1))
    for i in range(2, n + 1):
        inv[i] = (p - p // i) * inv[p % i] % p
    return inv


def quick_pow(a: int, n: int, p: int) -> int:
    """
    快速幂计算 a ^ n % p
    :param a: 底数
    :param n: 次数
    :param p: mod
    :return:
    """
    result = 1
    a = (a % p + p) % p
    while n:
        if n & 1:
            result = (a * result) % p
            a = (a * a) % p
        n >>= 1
    return result


def inverse_list(a: List[int], p: int) -> List[int]:
    """
    求任意 n 个数的逆元
    :param a:
    :param p:
    :return:
    """
    n = len(a)
    s = [1] * n
    sv = [1] * n
    inv = [1] * n
    for i in range(1, n + 1):
        s[i] = s[i - 1] * a[i] % p
    sv[n] = quick_pow(s[n], p - 2, p)
    for i in range(n, 0, -1):
        sv[i - 1] = sv[i] * a[i] % p
    for i in range(1, n + 1):
        inv[i] = sv[i] * s[i - 1] % p
    return inv


def crt(k: int, r: List[int], a: List[int]) -> int:
    """
    中国剩余定理
    :param k: 数组长度
    :param r: 余数数组
    :param a: 质数数组
    :return:
    """
    n = 1
    result = 0
    for i in range(k):
        n = n * a[i]
    for i in range(k):
        m = n // a[i]
        d, b, y = ex_gcd(m, a[i])
        result = (result + r[i] * m * b % n) % n
    return (result % n + n) % n
