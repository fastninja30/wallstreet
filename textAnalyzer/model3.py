import sqlite3
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


# Establish a connection to the database
conn = sqlite3.connect('../data/postDB.db')

# Get the list of all tables in the database
query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(query, conn)

# Print the names of all tables and their first few rows, shape, and size
for table in tables['name']:
    print(f"Table: {table}")
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    print("Columns:", df.columns.tolist())
    print(f"Shape: {df.shape}")
    print(f"Size: {df.size}")
    print("First few rows:")
    print(df.head())
    print("\n")


# Load comments to get user-post interactions
comments = pd.read_sql_query("SELECT author, post_id FROM comments", conn)

# Drop rows where author or post_id is None
comments.dropna(subset=['author', 'post_id'], inplace=True)

# Creating a bipartite graph
B = nx.Graph()
# Add nodes with the node attribute "bipartite"
B.add_nodes_from(comments['author'].unique(), bipartite=0)  # Users
B.add_nodes_from(comments['post_id'].unique(), bipartite=1)  # Posts

# Add edges based on comments table
edges = comments.apply(lambda x: (x['author'], x['post_id']), axis=1)
B.add_edges_from(edges)

# Create a projection of the bipartite graph for just the users
user_projection = nx.projected_graph(B, comments['author'].unique())

# Calculate degree centrality for the user projection
degree_centrality = nx.degree_centrality(user_projection)

# Convert the centrality dictionary to a DataFrame for easier handling
centrality_df = pd.DataFrame(list(degree_centrality.items()), columns=['author', 'degree_centrality'])

# Sort users by their centrality score
centrality_df = centrality_df.sort_values(by='degree_centrality', ascending=False)

# Print the scores
print(centrality_df)

# Close the connection
conn.close()
