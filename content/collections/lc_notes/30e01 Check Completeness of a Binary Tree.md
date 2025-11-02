---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 30e01
status: done
tags:
- binary tree
title: Check Completeness of a Binary Tree
---

## Check Completeness of a Binary Tree [LC#958]
> Given the root of a binary tree, determine if it is a complete binary tree. In a complete binary tree, every level, except possibly the last, is completely filled, and all nodes in the last level are as far left as possible. It can have between 1 and 2h nodes inclusive at the last level h.

### Intuition
- We do a BFS of the tree. This traverses the tree level by level.
- We should not encounter a null/empty node twice before queue is empty.

### Code
```python
def is_complete_tree(root: Optional[TreeNode]) -> bool:
    queue = deque([root])
    null_found = False
    while queue:
        node = queue.popleft()
        if node:
            if null_found:
                return False
            else:
                queue.append(node.left)
                queue.append(node.right)
        else:
            null_found = True
    return True
```

### Time complexity
- $T(n) = O(n)$
- $S(n) = O(n)$