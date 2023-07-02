#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: count for primes
@file_name: Primes.py
@project: Algorithm
@version: 1.0
@date: 2023/7/2 12:02
@author: air
"""


def linear_primes(n: int) -> tuple[int, list[int]]:
    """
    return count of primes from [1, n] and list of primes
    :param n: right range
    :return:
    """
    n = max(2, n)
    primes = n * [0]
    count = 0
    is_prime = [0] * 2 + [1] * (n - 1)
    
    for i in range(2, n):
        if is_prime[i]:
            primes[count] = i
            count += 1
        for j in range(count):
            if primes[j] * i >= n:
                break
            is_prime[primes[j] * i] = 0
            if not i % primes[j]:
                break
    return count, primes
