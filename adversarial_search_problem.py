
import city_node_list

class AdversarialSearch:
    def __init__(self, coffee_place, terminal_utilites, 
                        terminal, graph_data1, graph_data2 ):
        self.coffee_location = coffee_place
        self.terminal_utilities = terminal_utilites
        self.terminals = terminal
        self.graph = graph_data1
        self.graph_1 = graph_data2

    def find_cities(self):
        is_max = True
        terminals_1 = []
        chosen_cities = []
        for i in range(0, len(self.terminals), 2):
            if is_max:
                if self.terminals[i] > self.terminals[i + 1]:
                    chosen_cities.append(self.terminal_utilities[i])
                else:
                    chosen_cities.append(self.terminal_utilities[i + 1])
                terminals_1.append(max(self.terminals[i], self.terminals[i + 1]))

        is_max = False
        chosen_cities_2 = []
        terminals_2 = []

        for i in range(0, len(terminals_1), 2):
            if not is_max:
                if terminals_1[i] > terminals_1[i + 1]:
                    chosen_cities_2.append(self.graph[chosen_cities[i + 1]])
                else:
                    chosen_cities_2.append(self.graph[chosen_cities[i]])
                terminals_2.append(min(terminals_1[i], terminals_1[i + 1]))

        max_city_ind = 0
        if terminals_2[1] > terminals_2[max_city_ind]:
            max_city_ind = 1
        if terminals_2[2] > terminals_2[max_city_ind]:
            max_city_ind = 2

        second_city = chosen_cities_2[max_city_ind]
        first_chosen_city = self.graph_1[second_city]

        third_city_options = self.coffee_location[second_city]
        third_city = None
        for c in third_city_options:
            if c in self.graph:
                third_city = c

        return first_chosen_city, second_city, third_city

if __name__ == "__main__":
    result = AdversarialSearch(  city_node_list.coffees_place_data,
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