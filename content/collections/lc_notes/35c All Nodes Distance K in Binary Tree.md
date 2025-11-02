---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 35c
status: done
tags:
- binary tree
- bfs
title: All Nodes Distance K in Binary Tree
---

## All Nodes Distance K in Binary Tree [LC#863]
> Given the root of a binary tree, the value of a target node target, and an integer k, return an array of the values of all nodes that have a distance k from the target node. You can return the answer in any order.

### Intuition
Nodes at distance `k` can be children of the node or can be be children of one of the ancestors of the node. But without parent pointers searching for children on ancestors is very inefficient. So we create auxillary struture to maintain parent pointers and then perform BFS on the induced graph. 

### Code
```python
def nodes_at_k_hops(root: TreeNode, target: TreeNode, k: int) -> List[int]:
    parent_node = {}

    def create_parent_node(parent, node):
        if node:
            parent_node[node] = parent
            create_parent_node(node, node.left)
            create_parent_node(node, node.right)

    create_parent_node(None, root)

    # BFS
    visited = set()
    queue = deque([(target, k)])
    answers = []
    while queue:
        node, distance = queue.popleft()
        if not node or node in visited:
            continue

        visited.add(node)

        if distance == 0:
            answers.append(node.val)
            continue

        queue.append((node.left, distance - 1))
        queue.append((node.right, distance - 1))
        queue.append((parent_node[node], distance - 1))
    return answers
```
### Time complexity
Parent pointer creation is $O(n)$ and takes $O(n)$ space. BFS takes simlar space and time. 

- $T(n) = O(n)$
- $S(n) = O(n)$