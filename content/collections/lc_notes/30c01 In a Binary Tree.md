---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 30c01
status: done
title: In a Binary Tree
---

## Lowest Common Ancestor of a Binary Tree [LC#236]
> Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree. According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”


### Code
```python
class Node:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def lowest_common_ancestor(root: "Node", p: "Node", q: "Node") -> "Node":
    def search(node):
        if node in [p, q, None]:
            return node
        left = search(node.left)
        right = search(node.right)
        if left and right:
            return node
        return left if left else right
    return search(root)
```

### Time complexity
- $T(n) = O(n)$ and $S(n)= O(n)$ for the recursion stack in worst case.


If nodes are not guranteed to be in the tree
```python
def lowest_common_ancestor(root: "Node", p: "Node", q: "Node") -> "Node":
    found = 0
    def search(node):
        nonlocal found
        if node is None: 
            return node

        if node in [p, q]:
            found += 1
            return node

        left = search(node.left)
        right = search(node.right)
        if left and right:
            return node
        return left if left else right

    node = search(root)
    if found >= 2:
        return node
    return None
```