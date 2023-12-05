import numpy as np
from collections import deque
import city_node_list
import util

class AStarSearch:
    def __init__(self, state_graph, heuristic):
        self.state_graph = state_graph
        self.heuristic = heuristic

    def path_cost(self, path):
        cost = 0
        for s in range(len(path) - 1):
            cost += self.state_graph[path[s]][path[s + 1]]
        return cost

    def search(self, start, goal, return_cost=False, return_nexp=False):
        frontier = util.Frontier_PQ(start)
        visited = set()
        prev = {start: None}
        while frontier.q:
            cost, curr = frontier.pop()
            visited.add(curr)
            if curr == goal:
                p = util.path(prev, curr)
                if return_nexp == False:
                    return (p, self.path_cost(p)) if return_cost else p
                else:
                    return (p, self.path_cost(p), len(visited)) if return_cost else (p, len(visited))
            for adj in self.state_graph[curr]:
                if adj not in visited:
                    new_cost = cost + self.state_graph[curr][adj] + self.heuristic(adj) - self.heuristic(curr)
                    if adj not in frontier.states:
                        prev[adj] = curr
                        frontier.add(adj, new_cost)
                    elif frontier.states[adj] > new_cost:
                        prev[adj] = curr
                        frontier.replace(adj, new_cost)

def heuristic(state):
    return city_node_list.herustics_moyale[state]

astar = AStarSearch(city_node_list.distances_cost, heuristic)
ret = astar.search("Addis Ababa", "Moyale", return_cost=True, return_nexp=True)

print("optimal path using A*:", ret[0])
print("optimal path cost using A*:", ret[1])
print("Number of states expanded during search using A*:", ret[2])

