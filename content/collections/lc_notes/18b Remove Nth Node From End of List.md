---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 18b
status: done
title: Remove Nth Node From End of List
tags:
- linked list
---

## Remove Nth Node From End of List [LC#19]
> Given the head of a linked list, remove the nth node from the end of the list and return its head.

### Code
```python
def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    fake_head = ListNode(0, head)
    P = fake_head
    while n>0 and P:
        P = P.next
        n=n-1
    if not P: return head # less than n nodes

    Q = fake_head
    while P.next:
        P = P.next
        Q = Q.next
    Q.next = Q.next.next
    return fake_head.next
```