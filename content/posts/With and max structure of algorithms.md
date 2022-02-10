---
title : With and max structure in Algorithms
tags: [algorithms]
date: 2021-04-30T05:04:51+05:30
draft: true
---

# Kadane's Algorithm
```python
def maxSubArraySum(a,size):
    ##Your code here
    max_sum,max_start,max_end = a[0],0,0
    max_sum_with,max_with_start,max_with_end = a[0],0,0

    for i,ele in enumerate(a[1:],1):
        if max_sum_with<=0:
            max_sum_with,max_with_start,max_with_end = ele,i,i
        else:
            max_sum_with,max_with_start,max_with_end = max_sum_with+ele,max_with_start,i

        if max_sum<max_sum_with:
            max_sum,max_start,max_end = max_sum_with,max_with_start,max_with_end

    return max_sum,max_start,max_end
```

# Diameter of a Binary Tree
```python
def tree_diameter(root):
    if root is None:return 0,0,0
    
    left_height,left_max_diameter,left_diameter_with_root = tree_diameter(root.left)
    
    right_height,right_max_diameter,right_diameter_with_root  = tree_diameter(root.right)
    
    diameter_with_root = left_height+1+right_height 
    
    max_diameter = max(l_largest,r_largest,t)
    height = max(left_height,right_height)+1
    return height,max_diameter,diameter_with_root
```


We can observe a common structure in both of these algorithm. *with and max* . 

While the computations is underway, both of them considers all the index/node in a particular order. For Kadane's, the indices are examined one after the other in a linear order while tree diameter computation does an inorder traversal of the tree.


While the algorithm is examining each elements, it always seems to compute 2 solutions. One where the solution must include the element. The "with" solution.  The other solution is the most optimum answer over all the elements seen so far. The "max" solution.


The max solution is then updated if the *with* solution turns out to be a better solution. 

I keep stumbling across this structure from time to time. These are just 2 examples. Have you seen this structure elsewhere? Let me know. 