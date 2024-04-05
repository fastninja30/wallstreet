import praw
import json
from collections import Counter
from datetime import datetime, timedelta
import requests

with open('../Credentials.json', 'r') as file:
    credentials = json.load(file)


reddit_creds = credentials['reddit_api']['3']



base_url = "https://www.googleapis.com/customsearch/v1"

reddit = praw.Reddit(
    client_id=reddit_creds['id'],
    client_secret=reddit_creds['SECRET_KEY'],
    password=reddit_creds['password'],
    user_agent="testscript by u/fakebot3",
    username=reddit_creds['username']
)


class Reddit_Posts:
    def __init__(self, num_posts=10, subreddit_name="wallstreetbets"):
        posts = reddit.subreddit(subreddit_name).hot(limit=num_posts)
        # !!!!!self.posts sorting by score takes long time
        print("Blocking on Generating posts")
        # unsorted hotpost
        self.posts = list(posts)
        # sorted hotpost
        # self.posts = sorted(posts, key=lambda x: x.score, reverse=True)
        print("Release")

    ### Specification ###
    # inputs:
    #   n: the number of the post
    # return: the author name of the n-th post
    # String
    def search_by_time_period(start_date = "20231203", end_date = "20240110"):
        article_ids = []
        num = 10
        while(int(start_date) < int(end_date) and num == 10):
            print(f'Request from Google: {start_date} {end_date}')
            params = {
                "key": "AIzaSyBG2uCYJDwpZLlVcsmracUk3zRSJZMpn98", # The API key
                "cx": "b3dc3b1ce374e440c", # The CSE ID
                "q": "reddit", # The search query
                "sort": f"date:r:{start_date}:{end_date}", # The date range filter
                "num": 10 # The number of results to return
            }
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                num = len(data["items"])
                for item in data["items"]:
                    article_ids.append(item['link'].split('/')[-3])
                    date_obj = datetime.strptime(item['snippet'][:12].lstrip().rstrip(), "%b %d, %Y")
                    start_date = max(date_obj.strftime("%Y%m%d"),start_date)
            else:
                print(f"Request failed with status code {response.status_code}")
        print("Finished all requests")
        return article_ids
    ### Updated Method ###
    # Calculate the post frequency, average upvotes per post, upvote to downvote ratio per post,
    # and average comments per post for each unique author in the specified time frame
    def get_all_authors_post_stats(self, time_frame_days):
        # Calculate the timestamp for the specified time frame
        timestamp_limit = datetime.utcnow() - timedelta(days=time_frame_days)
        timestamp = int(timestamp_limit.timestamp())
        # Initialize dictionaries to store post statistics for each author
        author_frequency = Counter()
        author_upvotes = Counter()
        author_downvotes = Counter()
        author_comments = Counter()
        # Iterate through posts and calculate post statistics for each author
        for post in self.posts:
            if post.created_utc > timestamp and post.author is not None:
                author_frequency[post.author.name] += 1
                author_upvotes[post.author.name] += post.ups
                author_downvotes[post.author.name] += post.downs
                author_comments[post.author.name] += post.num_comments + len(post.comments.list())

        # Calculate average upvotes per post, upvote to downvote ratio per post,
        # and average comments per post for each author
        author_average_upvotes = {author: (upvotes / frequency) if frequency > 0 else 0
                                  for author, frequency in author_frequency.items()
                                  for upvotes in [author_upvotes[author]]}
        
        author_upvote_to_downvote_ratio = {author: (upvotes / max(downvotes, 1))  # Avoid division by zero
                                           for author, upvotes in author_upvotes.items()
                                           for downvotes in [author_downvotes[author]]}

        author_average_comments = {author: (comments / frequency) if frequency > 0 else 0
                                   for author, frequency in author_frequency.items()
                                   for comments in [author_comments[author]]}

        return dict(author_frequency), author_average_upvotes, author_upvote_to_downvote_ratio, author_average_comments, 

    weights = {
        'frequency': 0.2,
        'upvotes': 0.4,
        'ratio': 0.3,
        'comments': 0.1
    }

    def calculate_author_scores(self, authors_frequency, authors_average_upvotes, authors_upvote_to_downvote_ratio, authors_average_comments):
        author_scores = {}

        for author in authors_frequency.keys():
            # Calculate scores for each criterion
            frequency_score = authors_frequency[author] * self.weights.get('frequency', 1)
            upvotes_score = authors_average_upvotes.get(author, 0) * self.weights.get('upvotes', 1)
            ratio_score = authors_upvote_to_downvote_ratio.get(author, 0) * self.weights.get('ratio', 1)
            comments_score = authors_average_comments.get(author, 0) * self.weights.get('comments', 1)

            # Combine scores using weights
            total_score = frequency_score + upvotes_score + ratio_score + comments_score

            # Store the total score for the author
            author_scores[author] = total_score

        return author_scores
    
    def get_top_posts_info(self, time_frame_days, num_comments, posts_per_author=1):
    # Get post statistics and author scores
        authors_frequency, authors_average_upvotes, authors_upvote_to_downvote_ratio, authors_average_comments = self.get_all_authors_post_stats(time_frame_days)

        # Calculate author scores
        author_scores = self.calculate_author_scores(authors_frequency, authors_average_upvotes, authors_upvote_to_downvote_ratio, authors_average_comments)
        
        # Sort authors based on their scores (descending order)
        sorted_authors = sorted(author_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Gather information for the top posts from the top authors
        top_posts_info = []
        
        for author, _ in sorted_authors[:5]:
            # Track the number of posts retrieved for the current author
            posts_retrieved = 0
            
            # Find posts by the current author
            for post_index in range(len(self.posts)):
                if self.get_author(post_index) == author:
                    # Get information for the current post
                    title = self.get_title(post_index)
                    content = self.get_content(post_index)
                    upvotes = self.get_upvotes(post_index)
                    downvotes = self.get_downvotes(post_index)
                    comments = self.get_comments(post_index, num_comments)
                    comment_data = []
                    for comment_info in comments:
                        comment_data.append({
                            'author': comment_info['author'],
                            'upvotes': comment_info['upvotes'],
                            'downvotes': comment_info['downvotes'],
                            'content': comment_info['content'],
                            'replies': comment_info['replies']
                        })
                    
                    # Store the information for the current post in a dictionary
                    top_posts_info.append({
                        'title': title,
                        'content': content,
                        'author': author,
                        'comments': comment_data,
                        'upvotes': upvotes,
                        'downvotes': downvotes
                    })
                    
                    posts_retrieved += 1
                    
                    if posts_retrieved >= posts_per_author:
                        break  # Move to the next author after retrieving the desired number of posts
           
            if len(top_posts_info) >= len(sorted_authors) * posts_per_author:
                break  # Exit loop if we have gathered enough posts
            if posts_retrieved < posts_per_author:
                print(f"Warning: Author '{author}' has fewer than {posts_per_author} posts.")
                    
        return top_posts_info
    
    def getGPTString(self, top_posts_info):
        gpt_strings = []  # List to store the GPT strings for each post
        
        for post_info in top_posts_info:
            title = post_info['title']
            content = post_info['content']
            author_name = post_info['author']
            upvotes = post_info['upvotes']
            downvotes = post_info['downvotes']
            
            gpt_string = f"Post Title: {title}\n"
            gpt_string += f"  Post Content: {content}\n"
            gpt_string += f"  Post Author: {author_name}\n"
            gpt_string += f"  Post Upvotes: {upvotes}\n"
            gpt_string += f"  Post Downvotes: {downvotes}\n"
            
            # Add comments and replies
            for comment_data in post_info['comments']:
                comment_author = comment_data['author']
                comment_content = comment_data['content']
                comment_upvotes = comment_data['upvotes']
                comment_downvotes = comment_data['downvotes']
                
                gpt_string += f"    Comment by {comment_author}: {comment_content}\n"
                gpt_string += f"    Comment Upvotes: {comment_upvotes}\n"
                gpt_string += f"    Comment Downvotes: {comment_downvotes}\n"
                
                # Add replies
                for reply in comment_data['replies']:
                    reply_author = reply['author']
                    reply_content = reply['content']
                    
                    gpt_string += f"      Reply by {reply_author}: {reply_content}\n"
            
            # Add the constructed string to the list
            gpt_strings.append(gpt_string)
        
        return gpt_strings


    ### Specification ###
    # inputs:
    #   n: the number of the post
    # return: the title of the n-th post
    # String
    def get_title(self, n):
        return self.posts[n].title
    
    def get_author(self, n):
        return self.posts[n].author

    ### Specification ###
    # inputs:
    #   n: the number of the post
    # return: the content of the n-th post (What the author says)
    # String
    def get_content(self, n):
        post = self.posts[n]
    # Check if the post is a text post
        if post.is_self:
            return post.selftext
        # Check if the post is an image post
        elif post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return f"Image URL: {post.url}"
        # Return None for other types of posts
        else:
            return None

    ### Specification ###
    # inputs:
    #   n: the number of the post
    # return: the content of the n-th post (What the author says)
    # List of String.   ["urls","urls"]
    def get_images(self, n):
        return self.posts[n].url.endswith(('.jpg', '.jpeg', '.png', '.gif'))

    ### Specification ###
    # inputs:
    #   n: the number of the post
    # return: the upvotes of the n-th post
    # String
    def get_upvotes(self, n):
        return self.posts[n].ups

    ### Specification ###
    # inputs:
    #   n: the number of the post
    # return: the downvotes of the n-th post
    # String
    def get_downvotes(self, n):
        return self.posts[n].downs

    ### Specification ###
    # inputs:
    #   n: the number of the post
    #   num_comments: number of top comments you want under that post
    # return: the comments of the n-th post
    # List of Comments Object
    #
    # These are elements inside comment (could be more)
    # comment.author
    # comment.body
    # comment.score
    # comment.downs
    def get_comments(self, n, num_comments):
        post = self.posts[n]
        post.comments.replace_more(limit=0)
        comments = sorted(post.comments.list(), key=lambda x: x.score, reverse=True)[:num_comments]

        comment_data = []
        for comment in comments:
            # comment_info is a dictionary containing information about the comment,
            # including the author, upvotes, downvotes, content, and replies.
            comment_info = {
                'author': comment.author,
                'upvotes': comment.score,
                'downvotes': comment.downs,
                'content': comment.body,
                'replies': self.get_comment_replies(comment, num_replies=3)  # Adjust the number of replies as needed
            }
            comment_data.append(comment_info)

        return comment_data
    
    def get_comment_replies(self, comment, num_replies):
        comment.replies.replace_more(limit=0)
        replies = comment.replies.list()[:num_replies]

        reply_data = []
        for reply in replies:
            reply_info = {
                'author': reply.author,
                'upvotes': reply.score,
                'downvotes': reply.downs,
                'content': reply.body
            }
            reply_data.append(reply_info)

        return reply_data

