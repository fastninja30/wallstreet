#import reddit_api
#import gpt_api


# Sample usages
#posts = reddit_api.get_hot_posts()
# print(posts.json())


#response, chat_history = gpt_api.get_response("What is RCOS")

#response, chat_history = gpt_api.get_response("What is WallStreetPulse")


import praw
import time
from collections import defaultdict

ID = "mGJKXOitGGulU5pBJ9Zmqg"
SECRIT_KEY = "zZR3V_O4kRdzjJqKZN9-oNluADiHfg"
user = "WallStreetPulse"
PASSWORD = "WSPdevteam"

reddit = praw.Reddit(
    client_id=ID,
    client_secret=SECRIT_KEY,
    username=user,
    password=PASSWORD,
    user_agent="testscript by u/fakebot3",
)

def calculate_score(submission, num_followers, num_posts, total_upvotes, weights):
    score = (weights[0] * submission.num_comments + weights[1] * num_followers + weights[2] * submission.score)
    return score

start_time = time.time() - 7*24*60*60

author_posts = defaultdict(int)
author_upvotes = defaultdict(int)

# Take user input for the weights
weights = list(map(float, input("Enter the weights for posts, followers, and upvotes, separated by spaces: ").split()))

for submission in reddit.subreddit("WallStreetbets").top(time_filter="week"):
    if submission.stickied == False and submission.created_utc >= start_time:
        num_followers = submission.author.followers
        author_posts[submission.author] += 1
        author_upvotes[submission.author] += submission.score
        num_posts = author_posts[submission.author]
        total_upvotes = author_upvotes[submission.author]
        score = calculate_score(submission, num_followers, num_posts, total_upvotes, weights)
        print("\nTitle: ", submission.title)
        print("Score: ", score)

#https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html    #praw.models.Subreddit







