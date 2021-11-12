#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 线段树/SegmentTree
@file_name: SegmentTree.py
@project: Algorithm
@version: 1.0
@date: 2021/11/12 22:41
@author: airmelt
"""

from typing import Callable, Any


class STNode:
    def __init__(self, left: int, right: int, value: Any = None) -> None:
        """
        :param left: 左边界
        :param right: 右边界
        :param value: 节点值(区间值)
        """
        self.l, self.r = left, right
        self.value = value
        # 左右儿子及父指针
        self.left = self.right = self.father = None
        # 用于区间和问题的延迟更新标记
        self.lazy = None

    def __repr__(self) -> str:
        return f'({self.l} ~ {self.r} : {self.value})'


class SegmentTree:
    def __init__(self, fr: int, to: int, when_reach_leaf: Callable[[int], Any],
                 collect: Callable[[Any, Any], Any], lazy_update: Callable[[STNode, Any], None] = None) -> None:
        """
        :param fr: 整个区间的起始, 闭区间
        :param to: 整个区间的终结, 闭区间
        :param when_reach_leaf: 一个函数，用于向线段树内的叶子赋值；传入叶子的索引所谓参数，返回一个任意值
        :param collect: 一个函数，左区间和右区间的聚合方法；传入左区间和右区间，返回一个任意值作为两区间的聚合结果 | 左右区间应具有自反性
        :param lazy_update: 延迟更新算法，如果需要实现乘法的区间修改，请手动指定，否则默认取None即可
        """
        assert fr <= to
        # 到达叶时的赋值函数, 向上递归时对左右节点值的收集函数(必须为一个自反函数)
        self.cal, self.collect = when_reach_leaf, collect
        # 构建根节点
        self.root = self.__create_tree(fr, to)
        # 默认的lazy更新方法
        self.lazy_update = self.__default_lazy_update if lazy_update is None else lazy_update

    def __create_tree(self, fr, to, parent: STNode = None) -> STNode:
        """
        构建[fr, to]的树
        :param fr: 整个区间的起始, 闭区间
        :param to: 整个区间的终结, 闭区间
        :param parent: 父结点
        :return:
        """
        node = STNode(fr, to)
        # 构建一个父指针
        node.father = parent
        if fr == to:
            # 到达叶节点，根据元线段的值 fr 构建叶节点
            node.value = self.cal(fr)
        else:
            mid = fr + ((to - fr) >> 1)
            # 构建左右子树
            node.left, node.right = self.__create_tree(fr, mid, node), self.__create_tree(mid + 1, to, node)
            # 后序收集区间值
            node.value = self.collect(node.left.value, node.right.value)
        return node

    def query(self, fr: int, to: int) -> Any:
        """
        区间查询 | O(logN)
        :param fr: 整个区间的起始, 闭区间
        :param to: 整个区间的终结, 闭区间
        :return:
        """
        assert self.root.l <= fr <= to <= self.root.r

        def dfs(node, _fr, _to) -> Any:
            # 下传懒惰标记，仅适用于区间和问题
            if node.lazy is not None:
                self.__push_down(node)

            cur_l, cur_r = node.l, node.r
            # 找到对应区间
            if cur_l == _fr and cur_r == _to:
                return node.value
            else:
                mid = cur_l + ((cur_r - cur_l) >> 1)
                # 在左区间
                if _to <= mid:
                    return dfs(node.left, _fr, _to)
                # 在右区间
                elif _fr > mid:
                    return dfs(node.right, _fr, _to)
                # 跨区间
                else:
                    return self.collect(dfs(node.left, _fr, mid), dfs(node.right, mid + 1, _to))

        return dfs(self.root, fr, to)

    def update(self, i: int, value: Any) -> None:
        """
        单点修改: 把元线段 [i, i] 的值修改为 value
        :param i: 需要修改的下标
        :param value: 对应的值
        :return:
        """
        assert self.root.l <= i <= self.root.r

        def dfs(node):
            l, r = node.l, node.r
            # 找到对应元线段
            if l == i == r:
                node.value = value
            else:
                mid = l + ((r - l) >> 1)
                # 在左区间
                if i <= mid:
                    dfs(node.left)
                # 在右区间
                elif i > mid:
                    dfs(node.right)
                # 后序收集区间值
                node.value = self.collect(node.left.value, node.right.value)

        dfs(self.root)

    # 加强内容 -- push_down及区间修改 -- #
    #   仅适用于区间和

    def modify(self, fr: int, to: int, offset: Any) -> None:
        """
        区间修改: 整个区间的每个值都偏移一个幅度 O(logN)
        :param fr: 整个区间的起始, 闭区间
        :param to: 整个区间的终结, 闭区间
        :param offset: 区间修改的偏移值
        :return:
        """
        # 简单判定是否为区间和问题
        assert self.collect(3527, 1007) == 3527 + 1007

        def dfs(node, _fr, _to):
            l, r = node.l, node.r
            # 找到对应区间
            if l == _fr and r == _to:
                self.lazy_update(node, offset)
            else:
                mid = l + ((r - l) >> 1)
                # 在左区间
                if _to <= mid:
                    dfs(node.left, _fr, _to)
                # 在右区间
                elif _fr > mid:
                    dfs(node.right, _fr, _to)
                # 跨区间
                else:
                    dfs(node.left, _fr, mid)
                    dfs(node.right, mid + 1, _to)
                # 后序收集区间值
                self.collect(node.left.value, node.right.value)

        dfs(self.root, fr, to)

    @classmethod
    def __default_lazy_update(cls, ch: STNode, lazy: Any):
        """
        懒更新
        :param ch: 结点
        :param lazy: 结点标记
        :return:
        """
        # (r - l + 1)为此区间的元线段数
        meta_size = (ch.r - ch.l + 1)
        ch.value += meta_size * lazy
        ch.lazy = ch.lazy + lazy if ch.lazy is not None else lazy

    def __push_down(self, node: STNode) -> None:
        """
        下移
        :param node: 结点
        :return:
        """
        # 非元线段
        if node.l != node.r:
            # 给左右子树下传延迟更新标记并更新其值
            self.lazy_update(node.left, node.lazy)
            self.lazy_update(node.right, node.lazy)
        # 元线段不用下传lazy标志, 当前节点的lazy标志可清零
        node.lazy = None
