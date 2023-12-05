import city_node_list
import util

class Graph:

    def __init__(self, city_node_dict):
        self.city_node_dict = city_node_dict

    def _path_cost(self, path):
        cost = 0
        for s in range(len(path) - 1):
            for edge in self.city_node_dict[path[s]]:
                if edge[0] == path[s + 1]:
                    cost += edge[1]
                    break
        return cost

    def uniform_cost(self, start, goal, return_cost):
        frontier = util.Frontier_PQ(start)
        visited = set()
        prev = {start: None}
        while frontier.q:
            cost, curr = frontier.pop()
            if curr == goal:
                p = util.path(prev, curr)
                return (p, self._path_cost(p)) if return_cost else p
            visited.add(curr)
            for adj, adj_cost in self.city_node_dict[curr]:
                if adj not in visited:
                    if adj not in frontier.states:
                        prev[adj] = curr
                        frontier.add(adj, cost + adj_cost)
                    elif frontier.states[adj] > cost + adj_cost:
                        prev[adj] = curr
                        frontier.replace(adj, cost + adj_cost)

    def calc_UCS(self, start, goals):
        goal_cost = dict()
        min_cost = float('inf')
        min_cost_city = None
        min_cost_path = None
        for goal in goals:
            path, cost = self.uniform_cost(start, goal, True)
            goal_cost[goal] = cost
            if cost < min_cost:
                min_cost = cost
                min_cost_city = goal
                min_cost_path = path
        return min_cost_city, min_cost_path, min_cost

if __name__ == '__main__':
    graph = Graph(city_node_list.city_node_ucs)
    print(graph.uniform_cost("Addis Ababa", "Shire", True))
    goals = ["Axum", "Gondar", "Lalibella", "Babile", "Jimma", "Bale", "Sof Oumer", "Arba Minchi"]
    start = "Addis Ababa"
    res = graph.calc_UCS(start,goals)
    print(res)
    goals = ["Axum", "Gondar", "Lalibella", "Babile", "Bale", "Sof Oumer"]
    start = "Arba Minchi"
    res = graph.calc_UCS(start,goals)
    print(res)
    goals = ["Axum", "Gondar", "Lalibella", "Babile", "Sof Oumer"]
    start = "Bale"
    res = graph.calc_UCS(start,goals)
    print(res)
    goals = ["Axum", "Gondar", "Lalibella", "Babile" ]
    start = "Sof Oumer"
    res = graph.calc_UCS(start,goals)
    print(res)
    goals = ["Axum", "Gondar", "Lalibella"]
    start =  "Babile" 
    res = graph.calc_UCS(start,goals)
    print(res)
    goals = ["Axum", "Gondar"]
    start =  "Lalibella" 
    res = graph.calc_UCS(start,goals)
    print(res)
    goals = ["Axum"]
    start =  "Gondar" 
    res = graph.calc_UCS(start,goals)
    print(res)