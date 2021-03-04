#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 前缀树/Trie
@file_name: Trie.py
@project: Algorithm
@version: 1.0
@date: 2021/03/04 19:32
@author: Air
"""

__author__ = 'Air'


class Trie:

    def __init__(self) -> None:
        """
        初始化前缀树
        """
        self.root = {}

    def insert(self, word: str) -> None:
        """
        向前缀树中插入单词
        :param word: 待插入的单词
        :return:
        """
        node = self.root
        for c in word:
            if c not in node.keys():
                node[c] = {}
            node = node[c]
        node['is_word'] = True

    def search(self, word: str) -> bool:
        """
        查找前缀树中是否包含单词
        :param word: 待查找的单词
        :return: 是否查找到单词
        """
        node = self.root
        for c in word:
            if c not in node.keys():
                return False
            node = node[c]
        return 'is_word' in node.keys()

    def start_with(self, prefix: str) -> bool:
        """
        检查是否有前缀
        :param prefix: 前缀
        :return: 是否有前缀
        """
        node = self.root
        for c in prefix:
            if c not in node.keys():
                return False
            node = node[c]
        return True
