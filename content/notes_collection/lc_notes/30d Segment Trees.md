---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 30d
status: doing
title: Segment Trees
---

# Segment Trees

The sum of the root vertex at index 1, the sums of its two child vertices at indices 2 and 3.

```python
class SegmentTree:
    def __init__(self, arr: List[int]):
        self.size = len(arr)
        self.tree = [0] * (4 * self.size)  # Allocate space for the segment tree
        self.build(arr, 1, 0, self.size - 1)

    def operator(self, a:int, b:int):
        return a+b

    def build(self, array: List[int], node: int, left: int, right: int):
        if left == right:
            self.tree[node] = array[left]
        else:
            mid = (left + right) // 2
            self.build(array, node * 2, left, mid)
            self.build(array, node * 2 + 1, mid + 1, right)
            self.tree[node] = self.operator(self.tree[node * 2], self.tree[node * 2 + 1])

    def query(self, node: int, left: int, right: int, query_left: int, query_right: int) -> int:
        if query_left > query_right:
            return 0
        if query_left == left and query_right == right:
            return self.tree[node]
        mid = (left + right) // 2
        return (self.sum(node * 2, left, mid, query_left, min(query_right, mid)) +
                self.sum(node * 2 + 1, mid + 1, right, max(query_left, mid + 1), query_right))

    def update(self, node: int, left: int, right: int, position: int, new_value: int):
        if left == right:
            self.tree[node] = new_value
        else:
            mid = (left + right) // 2
            if position <= mid:
                self.update(node * 2, left, mid, position, new_value)
            else:
                self.update(node * 2 + 1, mid + 1, right, position, new_value)
            self.tree[node] = self.operator(self.tree[node * 2], self.tree[node * 2 + 1])

    def range_query(self, query_left: int, query_right: int) -> int:
        return self.query(1, 0, self.size - 1, query_left, query_right)

    def point_update(self, position: int, new_value: int):
        self.update(1, 0, self.size - 1, position, new_value)
```