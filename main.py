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

from redditData.Reddit_Posts import Reddit_Posts
from datetime import datetime, timedelta


def main():
    posts = Reddit_Posts(num_posts=50, subreddit_name="wallstreetbets")
    time_frame_days = 5
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
    article_ids = posts.search_by_time_period()
    post_urls = posts.get_all_post_urls(article_ids)
    author_stats = posts.get_all_authors_post_stats_from_urls(post_urls)
    print("Author Statistics:")
    for author, frequency in author_stats['author_frequency'].items():
        print(f"Author: {author}")
        print(f"  Post Frequency: {frequency}")
        print(f"  Average Upvotes per Post: {author_stats['author_average_upvotes'].get(author, 0)}")
        print(f"  Upvote to Downvote Ratio: {author_stats['author_upvote_to_downvote_ratio'].get(author, 0)}")
        print(f"  Average Comments per Post: {author_stats['author_average_comments'].get(author, 0)}")
        print()

if __name__ == "__main__":
    main()
#https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html    #praw.models.Subreddit







