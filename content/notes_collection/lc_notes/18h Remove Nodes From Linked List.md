---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 18h
status: done
tags:
- monotonic stack
- linked list
title: Remove Nodes From Linked List
---

## Remove Nodes From Linked List [LC#2487]
> You are given the head of a linked list. Remove every node which has a node with a greater value anywhere to the right side of it. Return the head of the modified linked list.

### Intuition
- Use a monotonic increasing stack. The nodes that are left on the stack is the answer.

### Code
```python
def remove_nodes(self, head: Optional[Node]) -> Optional[Node]:
    stack = []
    node = head
    while node:
        while stack and node and stack[-1].val < node.val:
            mid = stack.pop()
        stack.append(node)
        node = node.next
    
    dummy = node = Node(0, None)
    for v in stack:
        node.next = v
        node = v
    return dummy.next
```

### Time complexity
- $T(n) = O(n)$ 
- $S(n) = O(n)$