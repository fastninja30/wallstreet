from redditData.reddit_api import Reddit_API
import google_search as gs
from turtle import *

# Initialization
api = Reddit_API()
article_ids = gs.search_by_time_period()
comments = []

# Create a list of all comments for all article ids retrieved
article_ids_size = len(article_ids)
for i in range(0, 1):
    post = api.get_post_data(article_ids[i], "1000")
    api.get_dicts(post[1], comments, article_ids[i], "1000")
    print(len(comments))

# Print comments
comments_size = len(comments)
for i in range(0, comments_size):
    print(comments[i].get('body'))





