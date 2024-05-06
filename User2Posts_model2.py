import networkx as nx
from localDatabase.SQL import *
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
    user_nodes = list(set(post['author'] if post['author'] is not None else 'none' for post in posts) |
                      set(comment['author'] if comment['author'] is not None else 'none' for comment in comments))

    B.add_nodes_from(post_nodes, bipartite=0)  # Post nodes
    B.add_nodes_from(comment_nodes, bipartite=0)  # Comment nodes
    B.add_nodes_from(user_nodes, bipartite=1)  # User nodes

    # Add edges from users to posts
    for post in posts:
        B.add_edge(post['author'] if post['author'] is not None else 'none', 'post_' + str(post['id']))

    # Add edges from users to comments
    for comment in comments:
        B.add_edge(comment['author'] if comment['author'] is not None else 'none', 'comment_' + str(comment['id']))

    return B

# Each post is assigned a score based on the number of comments it has.
def calculate_post_scores(posts, comments):
    # Calculate post scores based on the number of comments
    post_scores = {str(post['id']): len([c for c in comments if c['post_id'] == post['id']]) for post in posts}
    return post_scores

# For each user, their initial score is calculated by summing up the scores of the posts they have interacted with (i.e., posted or commented on).
# This score represents the user's influence based on their interactions with influential posts.
def calculate_user_scores(bipartite_graph, post_scores):
    user_scores = {}
    for user in [n for n, d in bipartite_graph.nodes(data=True) if d['bipartite'] == 1]:
        user_post_scores = [post_scores.get(n.split('_')[1], 0) for n in bipartite_graph.neighbors(user) if n.startswith('post_')]
        user_scores[user] = sum(user_post_scores)
    return user_scores

# Each comment is assigned a score based on the post score it belongs to and the user score of the user who made the comment.
# This score represents the influence of the comment based on the influence of the post and the user.
def calculate_comment_scores(comments, post_scores, user_scores):
    comment_scores = {}
    for comment in comments:
        post_score = post_scores.get(str(comment['post_id']), 0)
        user_score = user_scores.get(comment['author'] if comment['author'] is not None else 'none', 0)
        comment_scores[str(comment['id'])] = post_score + user_score
    return comment_scores

# The user scores are updated by incorporating the scores of the comments they have made.
def update_user_scores(bipartite_graph, user_scores, comment_scores):
    for user in [n for n, d in bipartite_graph.nodes(data=True) if d['bipartite'] == 1]:
        user_comment_scores = [comment_scores.get(n.split('_')[1], 0) for n in bipartite_graph.neighbors(user) if n.startswith('comment_')]
        user_scores[user] += sum(user_comment_scores)
    return user_scores

def normalize_user_scores(user_scores):
    # Some normoalizing algo
    return user_scores

if __name__ == "__main__":
    sql = SQL("postDB.db")
    posts = sql.search("posts_info")
    comments = sql.search("comments")
    unique_comments = {}
    for comment in comments:
        body = comment['body']
        score = int(comment['score'])
        if body not in unique_comments or score > int(unique_comments[body]['score']):
            unique_comments[body] = comment

    comments = list(unique_comments.values())

    post_scores = calculate_post_scores(posts, comments)
    bipartite_graph = create_bipartite_graph(posts, comments)
    user_scores = calculate_user_scores(bipartite_graph, post_scores)
    comment_scores = calculate_comment_scores(comments, post_scores, user_scores)
    user_scores = update_user_scores(bipartite_graph, user_scores, comment_scores)
    user_scores = normalize_user_scores(user_scores)

    # User Score = Sum of Post Scores (the user interacted with) + Sum of Comment Scores
    sorted_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
    for user, score in sorted_scores:
        print(f"{user}: {score}")

    import json
    with open("model2_results.json", "w") as json_file:
        json.dump(sorted_scores, json_file, indent=4)