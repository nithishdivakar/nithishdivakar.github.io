---
date: 2024-01-01 00:00:00 +0000
layout: post
level: h1
slug: '73'
status: done
title: DSU Union-Find
---

## DSU Union-Find

```python
class DSU:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, x):
        if x not in self.parent:
            # new node
            self.parent[x] = x
            self.rank[x] = 0
            
        if self.parent[x] != x:
            # path compression
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x 

        self.parent[root_y] = root_x

        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        return True
```