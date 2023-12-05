import subprocess
import sys
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import city_node_list
import ucs_problem
import a_star_travel_et
import adversarial_search_problem

class CityGraph:
    def __init__(self, city_grapy):
        self.connections = city_grapy

    def cities(self):
        return list(self.connections.keys())

    def get(self, a, b=None):
        links = self.connections.get(a)
        if b is None:
            return links
        
class StateSpaceSearch:
    def __init__(self, city_graph=None, initial_state=None, goal_state=None, strategy=None,):
        self.city_graph = city_graph
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.strategy = strategy

    def search(self):
        if self.strategy == 'BFS':
            return self.breadth_first_search()
        elif self.strategy == 'DFS':
            return self.depth_first_search()
        elif self.strategy == 'UCS':
            return self.uniform_cost_search()
        elif self.strategy == 'CALCULAT_UCS':
            return self.calculate_ucs()
        elif self.strategy == 'ASTARS':
            return self.astar_search()
        elif self.strategy == 'ADVERSARIALS':
            return self.adversarial_search()
        else:
            raise ValueError('Invalid search strategy. Please choose either "BFS" or "DFS".')

    def breadth_first_search(self):
        visited = set()
        queue = [[self.initial_state]]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node == self.goal_state:
                return path

            if node not in visited:
                visited.add(node)
                neighbors = self.city_graph.get(node)

                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

        return None

    def depth_first_search(self):
        visited = set()
        stack = [[self.initial_state]]

        while stack:
            path = stack.pop()
            node = path[-1]

            if node == self.goal_state:
                return path

            if node not in visited:
                visited.add(node)
                neighbors = self.city_graph.get(node)

                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    stack.append(new_path)

        return None
    
    def uniform_cost_search(self):
        graph = ucs_problem.Graph(city_node_list.city_node_ucs)
        solution, cost = graph.uniform_cost(self.initial_state, self.goal_state, True)
        return solution
    
    def calculate_ucs(self):
        graph = ucs_problem.Graph(city_node_list.city_node_ucs)
        goals = ["Axum", "Gondar", "Lalibella", "Babile", "Jimma", "Bale", "Sof Oumer", "Arba Minchi"]
        start = "Addis Ababa"
        result = graph.calc_UCS(start, goals)
        print(result)
        goals = ["Axum", "Gondar", "Lalibella", "Babile", "Bale", "Sof Oumer"]
        start = "Arba Minchi"
        result = graph.calc_UCS(start,goals)
        print(result)
        goals = ["Axum", "Gondar", "Lalibella", "Babile", "Sof Oumer"]
        start = "Bale"
        result = graph.calc_UCS(start,goals)
        print(result)
        goals = ["Axum", "Gondar", "Lalibella", "Babile" ]
        start = "Sof Oumer"
        result = graph.calc_UCS(start,goals)
        print(result)
        goals = ["Axum", "Gondar", "Lalibella"]
        start =  "Babile" 
        result = graph.calc_UCS(start,goals)
        print(result)
        goals = ["Axum", "Gondar"]
        start =  "Lalibella" 
        result = graph.calc_UCS(start,goals)
        # print(result)
        goals = ["Axum"]
        start =  "Gondar" 
        result = graph.calc_UCS(start,goals)
        # print(result)
        return (result)
    
    def astar_search(self):
        astar = a_star_travel_et.AStarSearch(city_node_list.distances_cost, a_star_travel_et.heuristic)
        ret = astar.search("Addis Ababa", "Moyale", return_cost=True, return_nexp=True)
        return ("optimal path using A*:", ret[0],
                "optimal path cost using A*:", ret[1],
                "Number of states expanded during search using A*:", ret[2])
    def adversarial_search(self):
        result = adversarial_search_problem.AdversarialSearch(  city_node_list.coffees_place_data,
                            city_node_list.terminal_utilities,
                            city_node_list.terminal,
                            city_node_list.graph_data1,
                            city_node_list.graph_data2
                            )
        first_city, second_city, third_city = result.find_cities()
        print("Addis Ababa")
        print(first_city)
        print(second_city)
        print(third_city)
    
def main(initial_state, goal_state, strategy):
    G = nx.DiGraph()
    if strategy != 'UCS'and strategy is not None:
        city = CityGraph(city_node_list.graph_data)
        searcher = StateSpaceSearch(city, initial_state, goal_state, strategy)
        for city, connections in city.connections.items():
            for connection in connections:
                G.add_edge(city, connection)
        solution = searcher.search()
    elif strategy == 'CALCULAT_UCS':
        searcher = StateSpaceSearch()
        solution = searcher.search() 
    elif strategy == 'ASTARS':
        searcher = StateSpaceSearch()
        solution = searcher.search() 
    elif strategy == 'ADVERSARIALS':
        searcher = StateSpaceSearch()
        solution = searcher.search()
    else:
        city = CityGraph(city_node_list.city_node_ucs)
        searcher = StateSpaceSearch(city, initial_state, goal_state, strategy)
        for city, connections in city.connections.items():
            for connection in connections:
                G.add_edge(city, connection[0])
        solution = searcher.search()
    if solution is None:
        solution_nodes = []
    else:
        solution_nodes = solution   
    # solution_nodes = solution  # List of solution path nodes
    
    node_color = {}
    for n in G.nodes():
        if n in solution_nodes and len(solution_nodes) > 0:
            node_color[n] = '#00FF00'  # Color solution nodes green
        else:
            node_color[n] = '#E6B8B7'  # Color other nodes pink

    plt.figure(figsize=(40, 40))
    st.set_option('deprecation.showPyplotGlobalUse', False)
    pos = nx.spring_layout(G, seed=34, k=0.1)
    nx.draw_networkx(G, pos, with_labels=True, node_size=4000,  font_size=10, font_weight='bold', node_color=[node_color[n] for n in G.nodes()],  width=2)

    if solution:
        # print(f"Solution found using {strategy}: {' -> '.join(solution)}")
        if strategy == 'CALCULAT_UCS':
            plt.close()
            solution = f"{solution}"
        elif strategy == 'ASTARS':
            plt.close()
            solution = f"{solution}"
        elif strategy == 'ADVERSARIALS':
            plt.close()
            solution = f"{solution}"
        else:
            # plt.suptitle(f"Solution found using {strategy}: {' -> '.join(solution)}", fontsize=25, y=0.86)
            pass
    else:
        print(f"No solution found using {strategy}")
    st.pyplot() 
    # plt.show()
    return solution

def run_app():
    city = CityGraph(city_node_list.graph_data)
    st.set_page_config(page_title="Traveling Ethiopia Search Problem", layout='wide')
    st.title("Traveling Ethiopia Search Problem")

    col1, col2, col3 = st.columns(3)

    # initial_state = col1.text_input("Initial State:")
    # goal_state = col2.text_input("Goal State:")
    initial_state = col1.selectbox("Initial State:",city.cities())
    goal_state = col2.selectbox("Goal State:",city.cities())

    strategy = col3.selectbox("Strategy:", ["BFS", "DFS", "UCS", "CALCULAT_UCS", "ASTARS", "ADVERSARIALS"])
    search_button = st.button("Search")

    if search_button:
        solution = main(initial_state, goal_state, strategy)

        if solution:
            if strategy == "CALCULAT_UCS":
                st.write(f"Solution found using {strategy}: {solution}")
            elif strategy == 'ASTARS':
                st.write(f"Solution found using {strategy}: {solution}")
            elif strategy == 'ADVERSARIALS':
                st.write(f"Solution found using {strategy}: {solution}")
            else:
                solution_str = ' -> '.join(solution)
                st.write(f"Solution found using {strategy}: {solution_str}")
        else:
            st.write(f"No solution found using {strategy}")

    st.write("")
    exit_button = st.button("Exit")
    if exit_button:
        st.stop()
    

if __name__ == "__main__":
    run_app()
    # cmd = [sys.executable, "-m", "streamlit", "run", 'streamlitApp.py']
    # subprocess.Popen(cmd)
    
# ```



# ```
# # streamlit run strealitApp.py
# ```

