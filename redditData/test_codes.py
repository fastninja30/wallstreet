# Since the Reddit API hasn't been tested and dataset has not stored in SQL yet,
# This test codes for now only serves a hypothotical purpose. In this file,
# We assume that our API team will feed us two graphs:

# table 1 for main post information: id, url, article id, poster username, post content, published date, visited date, upvotes.
#downvotes comment replies to a previous comment), upvotes, downvotes
# table 2 for comments; id, article id(to know which post this comment is under), username, content, parent, comment id.
import pandas as pd
import User2User
import User2Posts

df_posts = pd.read_csv('posts.csv')
df_comments = pd.read_csv('comments.csv')

# Convert DataFrame to list of dictionaries
posts = df_posts.to_dict(orient='records')
comments = df_comments.to_dict(orient='records')

graph = User2User.create_interaction_graph(posts, comments)

initial_engagement_size = 10
spread_chance = 10  # Chance of spreading to another user (in percentage)
disengagement_chance = 30  # Chance of disengaging from the topic (in percentage)
immunity_chance = 20  # Chance of becoming immune after disengagement (in percentage)
check_frequency = 1  # How often each user checks for topic spread

# Run the simulation
results = User2User.simulate_topic_spread(graph, initial_engagement_size, spread_chance, disengagement_chance,
                                          immunity_chance, check_frequency)

engaged_users = [user for user, info in results.items() if info['engaged']]
immune_users = [user for user, info in results.items() if info['immune']]

print(f"Engaged Users: {engaged_users}")
print(f"Immune Users: {immune_users}")


from operator import itemgetter

# Get user nodes only
user_nodes = [n for n, d in User2Posts.bipartite_graph.nodes(data=True) if d['bipartite'] == 1]

# Calculate the degree of each user node
user_degrees = User2Posts.bipartite_graph.degree(user_nodes)
sorted_user_degrees = sorted(user_degrees, key=itemgetter(1), reverse=True)

print("Top 5 active users by connections:")
print(sorted_user_degrees[:5])



