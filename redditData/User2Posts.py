import networkx as nx
import pandas as pd

def create_bipartite_graph(posts, comments):
    """
    Creates a bipartite graph from posts and comments data.

    Args:
        posts (list of dicts): List containing post data.
        comments (list of dicts): List containing comment data.

    Returns:
        nx.Graph: A bipartite graph where one set of nodes are users and the other set are posts/comments.
    """
    B = nx.Graph()

    # Add nodes with the node attribute "bipartite"
    post_nodes = ['post_' + str(post['id']) for post in posts]
    comment_nodes = ['comment_' + str(comment['id']) for comment in comments]
    user_nodes = list(set(post['poster username'] for post in posts) | set(comment['username'] for comment in comments))

    B.add_nodes_from(post_nodes, bipartite=0)  # Post nodes
    B.add_nodes_from(comment_nodes, bipartite=0)  # Comment nodes
    B.add_nodes_from(user_nodes, bipartite=1)  # User nodes

    # Add edges from users to posts
    for post in posts:
        B.add_edge(post['poster username'], 'post_' + str(post['id']))

    # Add edges from users to comments
    for comment in comments:
        B.add_edge(comment['username'], 'comment_' + str(comment['id']))

    return B

# Convert DataFrame to list of dictionaries if not already done
posts = df_posts.to_dict(orient='records')
comments = df_comments.to_dict(orient='records')

# Create the bipartite graph
bipartite_graph = create_bipartite_graph(posts, comments)
