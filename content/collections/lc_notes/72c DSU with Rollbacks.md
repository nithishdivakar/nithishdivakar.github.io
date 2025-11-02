---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 72c
status: done
title: DSU with Rollbacks
---

## DSU with Rollbacks

- We do not add path compression as addition of roll back will results in unnecessary operations. This results in O(log n) for find (due to merge by rank)

```python
class DSU_rollback:
    def __init__(self):
        self.parent = {}
        self.rank = {}
        self.history = []

    def find(self, v):
        if v not in self.parent:
            self.parent[v] = v
            self.rank[v] = 0
      
        if v == self.parent[v]:
            return v
        # self.parent[v] = self.find(self.parent[v])
        # We don't perform path compression
    
        return self.find(self.parent[v])

    def union(self, v, u):
        v = self.find(v)
        u = self.find(u)
        if v == u:
            return False
        if self.rank[v] > self.rank[u]:
            v, u = u, v
        
        self.history.append((v, self.rank[v], u, self.rank[u]))
        
        self.parent[v] = u
        if self.rank[v] == self.rank[u]:
            self.rank[u] += 1
        return True

    def rollback(self):
        if not self.history:
            return
        v, rank_v, u, rank_u = self.history.pop()
        self.parent[v] = v
        self.rank[v] = rank_v
        self.parent[u] = u
        self.rank[u] = rank_u
```