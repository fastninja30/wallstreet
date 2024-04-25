from redditData.google_search import search_by_time_period
from redditData.reddit_api import Reddit_API
import SQLjsonHelper
import sqlite3
import sqlite3



def get_post_info(start_date="20231203", end_date="20240110"):
    # Get article IDs using custom search engine
    article_ids = search_by_time_period(start_date, end_date)
    
    # Initialize Reddit API
    api = Reddit_API()
    
    # Initialize SQLite connection
    conn = sqlite3.connect('reddit_data.db')
    cursor = conn.cursor()
    
    # Create main post information table
    cursor.execute('''CREATE TABLE IF NOT EXISTS main_posts (
                        id INTEGER PRIMARY KEY,
                        url TEXT,
                        article_id TEXT,
                        poster_username TEXT,
                        post_content TEXT,
                        published_date TEXT,
                        visited_date TEXT,
                        upvotes INTEGER,
                        downvotes INTEGER
                    )''')
    
    # Create comments table
    cursor.execute('''CREATE TABLE IF NOT EXISTS comments (
                        id INTEGER PRIMARY KEY,
                        article_id TEXT,
                        username TEXT,
                        content TEXT,
                        parent_comment_id INTEGER,
                        upvotes INTEGER,
                        downvotes INTEGER
                    )''')
    
    # Iterate through article IDs and fetch post information
    for article_id in article_ids:
        post_data = api.get_post_data(article_id, "1000")
        if post_data:
            post_info = api.get_post_dict(post_data[0])
            if post_info:
                # Insert main post information into main_posts table
                cursor.execute('''INSERT INTO main_posts (url, article_id, poster_username, post_content, 
                                                        published_date, visited_date, upvotes, downvotes)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                (post_info['url'], article_id, post_info['author'], 
                                post_info['selftext'], post_info['created_utc'], 
                                post_info['created_utc'], post_info['ups'], 
                                post_info['downs']))
                
                # Insert comments into comments table
                # for comment in post_info['comments']:
                #     cursor.execute('''INSERT INTO comments (article_id, username, content, 
                #                                             parent_comment_id, upvotes, downvotes)
                #                     VALUES (?, ?, ?, ?, ?, ?)''',
                #                     (article_id, comment['author'], comment['body'], 
                #                     comment['parent_id'], comment['score'], 
                #                     comment['downs']))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    get_post_info()


