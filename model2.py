import networkx as nx
import numpy as np

def calculate_user_scores(graph):
    """
    Calculates user scores based on a bipartite graph.

    Args:
        graph (nx.Graph): A bipartite graph with user nodes and post nodes.

    Returns:
        dict: A dictionary mapping user nodes to their scores.
    """
    user_scores = {}

    user_nodes = {node for node, data in graph.nodes(data=True) if data.get("bipartite") == 0}
    post_nodes = {node for node, data in graph.nodes(data=True) if data.get("bipartite") == 1}

    for user in user_nodes:
        #get neighbors (posts) of the user
        neighbors = list(graph.neighbors(user))

        #filter neighbors to include only post nodes and retrieve their scores
        post_neighbors = [node for node in neighbors if graph.nodes[node].get("bipartite") == 1]
        post_scores = [graph.nodes[post].get("score", 0) for post in post_neighbors]

        #check if post_scores is not empty before calculating the mean
        if post_scores:
            user_score = np.mean(post_scores)
        else:
            user_score = 0

        #store user score
        user_scores[user] = user_score

    return user_scores

def create_bipartite_graph(nodes_user, nodes_post, avg_degree):
    """
    Create a bipartite graph with specified numbers of user and post nodes and average degree.

    Args:
        nodes_user (int): Number of user nodes in the graph.
        nodes_post (int): Number of post nodes in the graph.
        avg_degree (float): Average degree of the nodes.

    Returns:
        nx.Graph: A bipartite graph.
    """
    graph = nx.Graph()
    graph.add_nodes_from(range(nodes_user), bipartite=0)  # User nodes
    graph.add_nodes_from(range(nodes_user, nodes_user + nodes_post), bipartite=1)  # Post nodes

    #assign scores to post nodes
    for post_node in range(nodes_user, nodes_user + nodes_post):
        graph.nodes[post_node]["score"] = np.random.randint(1, 11)  #PLACEHOLDER: change to whatever is needed parameter-wise

    #ensure a minimum number of connections for user nodes
    min_connections = avg_degree * nodes_user
    while graph.number_of_edges() < min_connections:
        user_node = np.random.randint(0, nodes_user)
        post_node = np.random.randint(nodes_user, nodes_user + nodes_post)
        graph.add_edge(user_node, post_node)

    return graph

if __name__ == "__main__":
    #create a bipartite graph
    graph_bipartite = create_bipartite_graph(nodes_user=1000, nodes_post=2000, avg_degree=5)

    #print the number of nodes and edges for the bipartite graph
    print("Bipartite Graph:")
    print("Number of user nodes:", len([n for n, d in graph_bipartite.nodes(data=True) if d["bipartite"] == 0]))
    print("Number of post nodes:", len([n for n, d in graph_bipartite.nodes(data=True) if d["bipartite"] == 1]))
    print("Number of edges:", graph_bipartite.number_of_edges())

    #calculate user scores based on the bipartite graph
    results = calculate_user_scores(graph_bipartite)
    print("User Scores:")
    for user, score in results.items():
        print(f"User {user}: {score}")
