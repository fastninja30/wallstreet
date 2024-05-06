import networkx as nx
import random
from tqdm import tqdm

random.seed(0)

def create_interaction_graph(posts, comments):
    """
    Creates a graph of user interactions based on posts and comments.

    Args:
        posts (list of dicts): List of post data dictionaries from the 'posts_info' table.
        comments (list of dicts): List of comment data dictionaries from the 'comments' table.

    Returns:
        nx.Graph: A graph where nodes are users and edges represent interactions.
    """
    graph = nx.Graph()

    # Add nodes for each unique user
    all_users = set([post['author'] for post in posts] + [comment['author'] for comment in comments])
    for user in all_users:
        user = "none" if user is None else user
        graph.add_node(user)

    # Add edges for post author and commenters
    for post in posts:
        post_author = post['author']
        for comment in comments:
            if comment['post_id'] == post['id']:
                commenter = comment['author']
                commenter = "none" if commenter is None else commenter
                post_author = "none" if post_author is None else post_author
                graph.add_edge(commenter, post_author)

    # Add edges for comment replies
    for comment in tqdm(comments):
        if comment['parent_id'] is not None and comment['parent_type'] == 'comment':
            parent_comment = next((c for c in comments if c['id'] == comment['parent_id']), None)
            if parent_comment:
                author = "none" if comment['author'] is None else comment['author']
                parent_author = "none" if parent_comment['author'] is None else parent_comment['author']
                graph.add_edge(author, parent_author)

    return graph


def simulate_topic_spread(posts, comments, initial_engaged_users, spread_chance, disengagement_chance, immunity_chance, check_frequency):
    all_users = set([post['author'] for post in posts] + [comment['author'] for comment in comments])
    node_statuses = {user if user is not None else "none": {"engaged": False, "immune": False, "check_timer": 0,
                                                            "engagement_score": 0} for user in all_users}
    engagement_scores = {"none" if user is None else user: 0 for user in all_users}

    # Initial engagement
    for user in initial_engaged_users:
        if user in node_statuses:
            user = "none" if user is None else user
            node_statuses[user]["engaged"] = True
    max_iter = 3 * (int(posts[-1]["created_date"]) - int(posts[0]["created_date"]))
    iteration = 0
    with tqdm(total=max_iter) as pbar_iter:
        while any(info["engaged"] for info in node_statuses.values()) and iteration < max_iter:
            for user, info in sorted(node_statuses.items()):
                if info["engaged"] and info["check_timer"] == 0:
                    if random.random() * 100 < disengagement_chance:
                        if random.random() * 100 < immunity_chance:
                            node_statuses[user]["immune"] = True
                        node_statuses[user]["engaged"] = False
                    info["check_timer"] = check_frequency
                elif info["check_timer"] > 0:
                    info["check_timer"] -= 1

            # Spread topic
            for post in posts:
                post_author = post['author']
                post_author = "none" if post_author is None else post_author
                if node_statuses[post_author]["engaged"]:
                    for comment in comments:
                        if comment['post_id'] == post['id']:
                            commenter = comment['author']
                            commenter = "none" if commenter is None else commenter
                            if not node_statuses[commenter]["immune"] and not node_statuses[commenter]["engaged"]:
                                if random.random() * 100 < spread_chance:
                                    node_statuses[commenter]["engaged"] = True
                                    engagement_scores[post_author] += 1

            for comment in comments:
                commenter = comment['author']
                commenter = "none" if commenter is None else commenter
                if node_statuses[commenter]["engaged"]:
                    if comment['parent_id'] is not None and comment['parent_type'] == 'comment':
                        parent_comment = next((c for c in comments if c['id'] == comment['parent_id']), None)
                        if parent_comment:
                            parent_author = parent_comment['author']
                            parent_author = "none" if parent_author is None else parent_author
                            if not node_statuses[parent_author]["immune"] and not node_statuses[parent_author]["engaged"]:
                                if random.random() * 100 < spread_chance:
                                    node_statuses[parent_author]["engaged"] = True
                                    engagement_scores[commenter] += 1
            iteration += 1
            pbar_iter.update(1)  # Update the outer progress bar for the iteration of the while loop

    return engagement_scores


# from redditData.User2User import create_interaction_graph, simulate_topic_spread
from localDatabase.SQL import *
sql = SQL("postDB.db")
posts = sql.search("posts_info", order_by="created_date ASC")
comments = sql.search("comments")
comments = sorted(comments, key=lambda x: x['id'])
# comments = comments[:1000]
print(len(posts), len(comments))


# Find the earliest post and its author
earliest_post = posts[0]['id']
initial_engaged_users = sql.search("comments", f"post_id = {earliest_post}")
initial_engaged_users = list({user['author'] for user in initial_engaged_users})

# Create the interaction graph
interaction_graph = create_interaction_graph(posts, comments)


# Simulate topic spread
spread_chance = 50
disengagement_chance = 5
immunity_chance = 0
check_frequency = 1

engagement_scores = simulate_topic_spread(posts, comments, initial_engaged_users, spread_chance, disengagement_chance, immunity_chance, check_frequency)

sorted_scores = sorted(engagement_scores.items(), key=lambda x: x[1], reverse=True)
for user, score in sorted_scores[:10]:
    print(f"User: {user}, Engagement Score: {score}")

with open("model1_results.json", "w") as json_file:
    json.dump(sorted_scores, json_file, indent=4)