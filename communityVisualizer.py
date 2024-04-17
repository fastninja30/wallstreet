import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import community as community_louvain

# Assuming df_posts and df_comments are your dataframes
df_posts = pd.DataFrame(
df_comments = pd.DataFrame()

# Create a directed graph
G = nx.DiGraph()

# Add nodes with the post information
for index, row in df_posts.iterrows():
    G.add_node(row['id'], type='post', poster_username=row['poster_username'])

# Add nodes with the comment information and edges from the post to the comment
for index, row in df_comments.iterrows():
    G.add_node(row['id'], type='comment', username=row['username'])
    G.add_edge(row['article_id'], row['id'])

# Function to visualize the graph
def visualize_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(20, 20))
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in G.nodes()})
    plt.axis('off')
    plt.show()

# Function to find the top k nodes with the most degrees
def top_k_nodes(G, k):
    degree_dict = dict(G.degree(G.nodes()))
    sorted_degree = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_degree[:k]

# Function to perform community detection
def detect_communities(G):
    # Convert to undirected graph for community detection
    undirected_G = G.to_undirected()
    partition = community_louvain.best_partition(undirected_G)
    return partition
    
# Function to add weighted edges based on interaction count
def add_weighted_edges(G, df_interactions):
    for index, row in df_interactions.iterrows():
        if G.has_edge(row['source_id'], row['target_id']):
            G[row['source_id']][row['target_id']]['weight'] += row['interaction_count']
        else:
            G.add_edge(row['source_id'], row['target_id'], weight=row['interaction_count'])

# Function to get the subgraph of a community
def get_community_subgraph(G, community_id, partition):
    nodes_in_community = [node for node in partition if partition[node] == community_id]
    return G.subgraph(nodes_in_community)
    
# Visualize the graph
visualize_graph(G)

# Print the top 5 nodes with the most degrees
print(top_k_nodes(G, 5))

# Print the communities
print(detect_communities(G))
