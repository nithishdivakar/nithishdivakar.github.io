---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 30a05
status: done
title: Binary Tree from its Traversals
---

## Construct Binary Tree from Preorder and Inorder Traversal [LC#105]
> Given two integer arrays `preorder` and `inorder` where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.

### Intuition
The elements in preorder represents the roots where the inorder traversal needs to be bifurcated. Maintaining a index map of inorder to quickly map to position of any element will allow quickly building the tree recursively.

### Code
```python
def build_tree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    val_to_idx = {val: idx for idx, val in enumerate(inorder)}

    def construct(in_left, in_right):
        if in_left > in_right:
            return None

        val = preorder.pop(0)
        in_idx = val_to_idx[val]
        node = TreeNode(val)

        node.left = construct(in_left, in_idx - 1)
        node.right = construct(in_idx + 1, in_right)
        return node
    return construct(0, len(preorder) - 1)
```

### Time Complexity

- $T(n) = O(n)$ and $S(n) = O(n)$ for the recursion stack