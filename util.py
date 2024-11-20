# util.py stores useful data structures

import sys
import heapq

class Stack:
    def __init__(self):
        self.list = []
    
    def push(self, item):
        self.list.append(item)
    
    def pop(self):
        return self.list.pop()
    
    def isEmpty(self):
        return len(self.list) == 0
    
class Queue:
    def __init__(self):
        self.list = []
    
    def push(self, item):
        self.list.insert(0, item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0
    
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0
    
    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count = self.count + 1
    
    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item
    
    def isEmpty(self):
        return len(self.heap) == 0

    


