import networkx as nx
import numpy as np

def calculate_user_scores(graph):
    """
    Calculates user scores based on a bipartite graph.

    Args:
        graph (nx.Graph): A bipartite graph with user nodes and post/comment nodes.

    Returns:
        dict: A dictionary mapping user nodes to their scores.
    """
    user_scores = {}

    # Assuming user nodes have bipartite=1
    user_nodes = {node for node, data in graph.nodes(data=True) if data["bipartite"] == 1}
    post_comment_nodes = {node for node, data in graph.nodes(data=True) if data["bipartite"] == 0}

    for user in user_nodes:
        # Get neighbors (posts/comments) of the user
        neighbors = list(graph.neighbors(user))

        # Calculate user score based on the average score of connected posts/comments
        post_scores = [graph.nodes[post]["score"] for post in neighbors if "score" in graph.nodes[post]]
        user_score = np.mean(post_scores) if post_scores else 0

        # Store user score
        user_scores[user] = user_score

    return user_scores
