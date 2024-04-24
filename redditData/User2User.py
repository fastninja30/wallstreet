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


def simulate_topic_spread(graph, initial_engagement_size, spread_chance, disengagement_chance, immunity_chance, check_frequency):
    """
    Simulates the spread of a topic or idea on a user interaction graph.

    Args:
        graph (nx.Graph): A graph representing interactions between users.
        initial_engagement_size (int): Number of users initially engaged with the topic.
        spread_chance (float): Probability of the topic spreading to another user.
        disengagement_chance (float): Probability of a user disengaging from the topic.
        immunity_chance (float): Probability of a user becoming immune to the topic.
        check_frequency (int): Frequency of engagement checks.

    Returns:
        dict: A dictionary mapping users to their engagement and immunity status.
    """
    node_statuses = {node: {"engaged": False, "immune": False, "check_timer": 0} for node in graph.nodes}

    # Initial engagement
    initial_engaged_users = random.sample(list(graph.nodes), initial_engagement_size)
    for user in initial_engaged_users:
        node_statuses[user]["engaged"] = True

    while any(info["engaged"] for info in node_statuses.values()):
        for user, info in node_statuses.items():
            if info["engaged"] and info["check_timer"] == 0:
                if random.random() * 100 < disengagement_chance:
                    if random.random() * 100 < immunity_chance:
                        node_statuses[user]["immune"] = True
                    node_statuses[user]["engaged"] = False
                info["check_timer"] = check_frequency
            elif info["check_timer"] > 0:
                info["check_timer"] -= 1

        # Spread topic
        for user in graph.nodes:
            if node_statuses[user]["engaged"]:
                neighbors = list(graph.neighbors(user))
                for neighbor in neighbors:
                    if not node_statuses[neighbor]["immune"] and not node_statuses[neighbor]["engaged"]:
                        if random.random() * 100 < spread_chance:
                            node_statuses[neighbor]["engaged"] = True

    return node_statuses