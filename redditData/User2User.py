import networkx as nx
import random

def create_interaction_graph(posts, comments):
    """
    Creates a graph of user interactions based on posts and comments.

    Args:
        posts (list of dicts): List containing post data, with each post including 'user' and 'post_id'.
        comments (list of dicts): List containing comment data, with each comment including 'user', 'post_id', and optionally 'reply_to'.

    Returns:
        nx.Graph: A graph where nodes are users and edges represent interactions.
    """
    graph = nx.Graph()
    user_interactions = {}

    # Add nodes for each user and record interactions from comments
    for post in posts:
        graph.add_node(post['user'])
        user_interactions[post['post_id']] = post['user']

    for comment in comments:
        graph.add_node(comment['user'])
        post_author = user_interactions[comment['post_id']]
        # Add an edge between the commenter and the post author
        graph.add_edge(comment['user'], post_author)

        # If the comment is a reply to another comment, add an edge to the user they are replying to
        if 'reply_to' in comment:
            reply_author = user_interactions.get(comment['reply_to'])
            if reply_author:
                graph.add_edge(comment['user'], reply_author)

    return graph
