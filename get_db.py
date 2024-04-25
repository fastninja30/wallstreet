from redditData.google_search import search_by_time_period
from redditData.reddit_api import Reddit_API
import SQLjsonHelper

def get_post_info(start_date="20231203", end_date="20240110"):
    article_ids = search_by_time_period(start_date, end_date)
    print(article_ids)
    api = Reddit_API()

    for article_id in article_ids:
        post_data = api.get_post_data(article_id, "1000")
        post_info = api.get_post_dict(post_data[0])

        # Insert post information into the 'redditPosts' table
        post_info_to_insert = {
            "id": post_info["id"],
            "url": post_info["url"],
            "article_id": article_id,
            "poster_username": post_info["author"],
            "post_content": post_info["content"],
            "published_date": post_info["published_date"],
            "visited_date": post_info["visited_date"],
            "upvotes": post_info["upvotes"],
            "downvotes": post_info["downvotes"]
        }
        SQLjsonHelper.add_post("redditPosts", post_info_to_insert)

        # Insert comments into the 'comments' table
        comments = post_info.get("comments", [])
        for comment in comments:
            comment_info_to_insert = {
                "id": comment["id"],
                "article_id": article_id,
                "username": comment["username"],
                "content": comment["content"],
                "parent_comment_id": comment.get("parent_comment_id", None),
                "upvotes": comment["upvotes"],
                "downvotes": comment["downvotes"]
            }
            SQLjsonHelper.add_comment("comments", comment_info_to_insert)
if __name__ == "__main__":
    get_post_info()
