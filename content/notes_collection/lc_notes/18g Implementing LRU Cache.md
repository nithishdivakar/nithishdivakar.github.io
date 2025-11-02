---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 18g
status: done
title: Implementing LRU Cache
tags:
- linked list
---

## Implementing LRU Cache [LC#146]
> Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
> 
> Implement the LRUCache class:
> - `LRUCache(int capacity)` Initialize the LRU cache with positive size capacity.
> - `int get(int key)` Return the value of the key if the key exists, otherwise return -1.
> - `void put(int key, int value)` Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.
> The functions get and put must each run in $O(1)$ average time complexity.

 
### Intuition
- Values can be stored in a dictionary
- For keeping track of freshness, we use a doubly linked list. 
    - New values are inserted at the right end
    - existing values are removed and nserted at the right end to implement recently used property
    - Capacity can be enforced by removing nodes from left. Nodes in the left are least recently used. 

### Code
```python
class Node:
    def __init__(self, key, val, nxt=None, prev=None):
        self.key = key
        self.val = val
        self.next = nxt
        self.prev = prev
    
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.storage = {}
        self.head = Node(-1, -1, None, None)
        self.tail = Node(-2, -2, None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_at_end(self, node):
        node.prev = self.tail.prev
        node.next = self.tail 
        self.tail.prev.next = node
        self.tail.prev = node

    def remove_node(self, node):
        node.next.prev = node.prev
        node.prev.next = node.next
        return node.key

    def get(self, key: int) -> int:
        if key in self.storage:
            # update freshness
            node = self.storage[key]
            self.remove_node(node)
            self.add_at_end(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.storage:
            self.storage[key].val = value
            self.get(key)
        else:
            node = Node(key, value, None, None)
            self.storage[key] = node
            self.add_at_end(node)
            if len(self.storage)>self.capacity:
                rm_key = self.remove_node(self.head.next)
                del self.storage[rm_key]     
```


### Time Complexity
- $O(1)$ for get and put 
- $O(n)$ storage for dictionary and linkeidnlist