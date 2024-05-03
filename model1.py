import networkx as nx
import random

def simulate_virus_spread(graph, initial_outbreak_size, virus_spread_chance, recovery_chance, gain_resistance_chance, virus_check_frequency):
    """
    Simulates the spread of a virus on a graph.

    Args:
        graph (nx.Graph): A graph representing connections between nodes.
        initial_outbreak_size (int): Number of initially infected nodes.
        virus_spread_chance (float): Probability of virus spreading to neighbors.
        recovery_chance (float): Probability of recovery from infection.
        gain_resistance_chance (float): Probability of gaining resistance after recovery.
        virus_check_frequency (int): Frequency of virus checks.

    Returns:
        dict: A dictionary mapping nodes to their infection status (infected, resistant).
    """
    node_statuses = {}

    #initialize nodes
    for node in graph.nodes:
        node_statuses[node] = {"infected": False, "resistant": False, "virus_check_timer": 0}

    #initial outbreak
    initial_infected_nodes = random.sample(list(graph.nodes), initial_outbreak_size)
    for node in initial_infected_nodes:
        node_statuses[node]["infected"] = True

    while any(info["infected"] for info in node_statuses.values()):
        for node, info in node_statuses.items():
            if info["infected"] and info["virus_check_timer"] == 0:
                if random.random() * 100 < recovery_chance:
                    if random.random() * 100 < gain_resistance_chance:
                        node_statuses[node]["resistant"] = True
                    node_statuses[node]["infected"] = False
                node_statuses[node]["virus_check_timer"] = virus_check_frequency
            elif info["virus_check_timer"] > 0:
                node_statuses[node]["virus_check_timer"] -= 1

        #spread virus
        for node in graph.nodes:
            if node_statuses[node]["infected"]:
                neighbors = list(graph.neighbors(node))
                for neighbor in neighbors:
                    if not node_statuses[neighbor]["resistant"]:
                        if random.random() * 100 < virus_spread_chance:
                            node_statuses[neighbor]["infected"] = True

    return node_statuses

if __name__ == "__main__":
    #test graph with 1000 nodes and an avg degree of 5
    test_graph = nx.fast_gnp_random_graph(n=1000, p=0.005, seed=42)

    influential_nodes = random.sample(list(test_graph.nodes()), 10)
    extra_connections = 20

    for node in influential_nodes:
        for _ in range(extra_connections):
            random_neighbor = random.choice(list(test_graph.nodes()))
            test_graph.add_edge(node, random_neighbor)

    #simulation parameters
    initial_outbreak_size = 10
    virus_spread_chance = 10 
    recovery_chance = 70  
    gain_resistance_chance = 50  
    virus_check_frequency = 1  

    # Simulate virus spread on the test graph
    results = simulate_virus_spread(test_graph, initial_outbreak_size, virus_spread_chance, recovery_chance, gain_resistance_chance, virus_check_frequency)

    # Print the results (infected and resistant nodes)
    print("Infected nodes:", [node for node, info in results.items() if info["infected"]])
    print("Resistant nodes:", [node for node, info in results.items() if info["resistant"]])
