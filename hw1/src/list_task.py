#!/usr/bin/env python
import pdb

# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    #pdb.set_trace()
    result = []

    if lst == None:
        return None
    else:
        prev = lst[0]
        result.append(lst[0])

    for a in lst:
        if prev != a:
            result.append(a)
        prev = a
    return result

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    l1 = len(lst1)
    l2 = len(lst2)
    result = []
    i = 0
    j = 0
    #pdb.set_trace()
    while( i < l1 and j < l2):
        if lst1[i] < lst2[j]:
            result.append(lst1[i])
            i += 1
        else:
            result.append(lst2[j])
            j += 1
    return result + lst1[i:] + lst2[j:]

lst = [1, 2, 2, 3]
print(remove_adjacent(lst))
print(linear_merge([2, 6], [1, 3, 5]))