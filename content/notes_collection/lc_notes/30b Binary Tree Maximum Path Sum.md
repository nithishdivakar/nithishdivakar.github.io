---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 30b
status: done
title: Binary Tree Maximum Path Sum
---

## Binary Tree Maximum Path Sum [LC#124]
> A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.
> 
> The path sum of a path is the sum of the node's values in the path. Given the root of a binary tree, return the maximum path sum of any non-empty path.

**Depth first traversal**
- The answer is inspired from  from Kadane's algorithm for max array sum
- At every node, we are looking for what is max path sum of the path ending at the node and containing only the node's children.
- Once we have that for both children, we can also calculate the max path sum of the path passing through the node.
- Keep track of the maximum of such path sum's
- $T(n) = O(n)$; $S(n) = O(h)$. recursion depth $\approx$ max height of the tree

```python
def binary_tree_max_path_sum(root: Optional[TreeNode]) -> int:
    ans = float('-inf')
    def ending_with(node):
        # What is the max path sum with path ending at node
        # and the path contains only node's children?

        nonlocal ans
        if not node: return 0

        left_gain = max(ending_with(node.left), 0)
        right_gain = max(ending_with(node.right), 0)

        # max path sum of path passing through node
        current_max = left_gain + node.val + right_gain

        ans = max(ans, current_max)

        node_gain = max(left_gain, right_gain) + node.val
        return node_gain

    ending_with(root)
    return ans
```