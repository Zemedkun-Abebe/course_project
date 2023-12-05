
import heapq

class Frontier_PQ():
    def __init__(self, start, cost = 0):
        self.start = start
        self.cost = cost
        self.states = {start:cost} # the explored nodes
        self.q = [[cost, start]] # the can-be-explored nodes
    
    def add(self,state,cost):
        self.states[state]=cost
        heapq.heappush(self.q,[cost,state])
    
    def pop(self):
        return heapq.heappop(self.q)
    
    def replace(self,state,cost):
        self.states[state]=cost
        for i,tup in enumerate(self.q):
            if tup[1]==state:
                self.q[i][0]=cost

def path(previous, s): 
    if s is None:
        return []
    else:
        return path(previous, previous[s])+[s]