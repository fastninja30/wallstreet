import sqlite3
import networkx as nx
import random
from tqdm import tqdm

conn = sqlite3.connect('postDB.db')
cursor = conn.cursor()
cursor.execute("SELECT author, post_id, parent_id, parent_type FROM comments")
comments_data = cursor.fetchall()

# Construct user-to-user graph
G = nx.DiGraph()
for author, post_id, parent_id, parent_type in tqdm(comments_data):
    if parent_type == 'comment':
        cursor.execute("SELECT author FROM comments WHERE id = ?", (parent_id,))
    else:  # parent_type == 'post'
        cursor.execute("SELECT author FROM posts_info WHERE id = ?", (post_id,))

    parent_author = cursor.fetchone()
    if parent_author:
        G.add_edge(parent_author[0], author)

# Define the simulation parameters
initial_infected_ratio = 0.01

random.seed(0)
def run_simulation(G, initial_infected_ratio, transmission_prob):
    for node in G.nodes():
        G.nodes[node]['state'] = 'infected' if random.random() < initial_infected_ratio else 'susceptible'

    new_infections = True
    while new_infections:
        new_infections = False
        for node in list(G.nodes()):
            if G.nodes[node]['state'] == 'infected':
                for neighbor in G.neighbors(node):
                    if G.nodes[neighbor]['state'] == 'susceptible' and random.random() < transmission_prob:
                        G.nodes[neighbor]['state'] = 'infected'
                        new_infections = True

    infected_count = sum(1 for node in G.nodes() if G.nodes[node]['state'] == 'infected')
    print(f" infested node counts: {infected_count}    Current transmission prob: {transmission_prob} Infersted ratio: {infected_count/len(G.nodes())} num_nodes:{len(G.nodes())}")
    return infected_count / len(G.nodes())


# determine the threshold for outbreak
def find_threshold(G, initial_infected_ratio, max_iterations=100):
    transmission_prob = 0.00
    for i in range(max_iterations):
        infection_ratio = run_simulation(G, initial_infected_ratio, transmission_prob)
        if infection_ratio > 0.5:  # If more than 50% are infected, outbreak is significant
            return transmission_prob
        transmission_prob += 0.001  # Increment the transmission probability


threshold = find_threshold(G, initial_infected_ratio)
print(f"Outbreak threshold: {threshold:.3f}")

conn.close()

'''
# Simulation without using a random initial infected node
# Initialize initial infected node using https://www.reddit.com/r/wallstreetbets/comments/l2x7he/gme_yolo_update_jan_22_2021/

import sqlite3
import networkx as nx
import random
from tqdm import tqdm

conn = sqlite3.connect('postDB.db')
cursor = conn.cursor()
cursor.execute("SELECT author, post_id, parent_id, parent_type FROM comments")
comments_data = cursor.fetchall()

# Find the earliest post and its author
cursor.execute("SELECT id, created_date FROM posts_info ORDER BY created_date ASC")
posts_data = cursor.fetchall()
earliest_post_id = posts_data[0][0]

# Retrieve users who interacted with the earliest post
cursor.execute("SELECT author FROM comments WHERE post_id = ?", (earliest_post_id,))
initial_infected_users = [row[0] for row in cursor.fetchall()]
initial_infected_users = ["none" if user is None else user for user in initial_infected_users]

# Construct user-to-user graph
G = nx.DiGraph()
for author, post_id, parent_id, parent_type in tqdm(comments_data):
    if parent_type == 'comment':
        cursor.execute("SELECT author FROM comments WHERE id = ?", (parent_id,))
    else:  # parent_type == 'post'
        cursor.execute("SELECT author FROM posts_info WHERE id = ?", (post_id,))

    parent_author = cursor.fetchone()
    author = "none" if author is None else author
    if parent_author:
        parent_author = "none" if parent_author[0] is None else parent_author[0]
        G.add_edge(parent_author, author)

random.seed(0)
# Define the simulation parameters
def run_simulation(G, initial_infected_users, transmission_prob):
    # Initialize the states of the nodes
    for node in G.nodes():
        G.nodes[node]['state'] = 'infected' if node in initial_infected_users else 'susceptible'

    new_infections = True
    while new_infections:
        new_infections = False
        for node in list(G.nodes()):
            if G.nodes[node]['state'] == 'infected':
                for neighbor in G.neighbors(node):
                    if G.nodes[neighbor]['state'] == 'susceptible' and random.random() < transmission_prob:
                        G.nodes[neighbor]['state'] = 'infected'
                        new_infections = True

    infected_count = sum(1 for node in G.nodes() if G.nodes[node]['state'] == 'infected')
    print(f" infested node counts: {infected_count}    Current transmission prob: {transmission_prob} Infersted ratio: {infected_count/len(G.nodes())} num_nodes:{len(G.nodes())}")

    return infected_count / len(G.nodes())

# determine the threshold for outbreak
def find_threshold(G, initial_infected_users, max_iterations=100):
    transmission_prob = 0.00
    for i in tqdm(range(max_iterations)):
        infection_ratio = run_simulation(G, initial_infected_users, transmission_prob)
        if infection_ratio > 0.5:  # If more than 50% are infected, outbreak is significant
            return transmission_prob
        transmission_prob += 0.0001  # Increment the transmission probability

threshold = find_threshold(G, initial_infected_users)
print(f"Outbreak threshold: {threshold:.4f}")


conn.close()



'''