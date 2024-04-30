from redditData.google_search import *
from datetime import datetime
from localDatabase.SQL import *
from tqdm import tqdm

import praw
import random
try:
    current_dir = os.getcwd()
    credentials_path = os.path.join(current_dir, '../Credentials.json')
    # Load credentials from the file
    with open(credentials_path, 'r') as file:
        credentials = json.load(file)
except:
    pass
try:
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to Credentials.json
    credentials_path = os.path.join(current_dir, '../Credentials.json')

    # Load credentials from the file
    with open(credentials_path, 'r') as file:
        credentials = json.load(file)
except:
    pass
base_url = "https://www.googleapis.com/customsearch/v1"
reddit_keys = list(credentials['reddit_api'].keys())
# reddit_creds = credentials['reddit_api'][random.choice(reddit_keys)]
reddit_creds = credentials['reddit_api']['2']
reddit = praw.Reddit(
    client_id=reddit_creds['id'],
    client_secret=reddit_creds['SECRET_KEY'],
    password=reddit_creds['password'],
    user_agent="testscript by u/fakebot3",
    username=reddit_creds['username']
)

def get_reddit_post_info(post_id):
    try:
        # Retrieve the post using the post ID
        post = reddit.submission(id=post_id)
        created_date = datetime.fromtimestamp(post.created_utc).strftime('%Y%m%d')
        # Retrieve the post information
        post_info = {
            'id': post.id,
            'title': post.title,
            'body': post.selftext,
            'author': post.author.name if post.author else None,
            'score': post.score,
            'url': post.url,
            'created_date': created_date,
            'num_comments': post.num_comments,
            'comments': []
        }

        # Retrieve the comments
        print("Retrieving", post.num_comments, "comments for", post_id)
        post.comments.replace_more(limit=None)  # Retrieve all comments, including nested ones
        for comment in post.comments.list():
            parent_id = comment.parent_id
            parent_type = 'post' if parent_id.startswith('t3_') else 'comment'
            parent_id = parent_id[3:]  # Remove the prefix (t1_ for comments, t3_ for posts)
            comment_created_date = datetime.fromtimestamp(comment.created_utc).strftime('%Y%m%d')
            comment_info = {
                'id': comment.id,
                'author': comment.author.name if comment.author else None,
                'body': comment.body,
                'score': comment.score,
                'created_date': comment_created_date,
                'post_id': post.id,
                'parent_id': parent_id,
                'parent_type': parent_type
            }
            post_info['comments'].append(comment_info)

        return post_info

    except Exception as e:
        print(f"Error retrieving post information: {str(e)}")
        return None


SQL = SQL("postDB.db")
# posts = SQL.search("google_search")
posts = SQL.search("google_search", "is_visited=False")
for post in tqdm(posts):
    post_info = get_reddit_post_info(post['id'])
    post_dict = {key: value for key, value in post_info.items() if key != 'comments'}
    SQL.insert("posts_info", post_dict)
    for comment in post_info['comments']:
        SQL.insert("comments", comment)
    SQL.update("google_search", {"is_visited": "True"}, f"id='{post['id']}'")

print("Finish")
