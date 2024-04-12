from redditData.reddit_api import Reddit_API

# Reddit API object
# https://www.reddit.com/r/wallstreetbets/comments/1axhn74/most_anticipated_earnings_releases_for_the_week/
api = Reddit_API()
post = api.get_post_data("1axhn74", "1000")

# Gets all comments and replies for hot posts
# for i in range(0, len(hot_posts.get('data').get('children'))):
#     data = api.get_post_data(api.get_post_id(hot_posts.get('data').get('children')[i]))
#     api.get_comments(data[1])

# The Post title and content
# print(api.get_post_title(post[0]))
# print(api.get_post_content(post[0]))

# Extracts a list of directories of comments and replies
comments = []
api.get_dicts(post[1], comments,"1axhn74","1000")
size = len(comments)
print(size)
# print(comments[1].keys())
# for i in range(0, size):
#     print(comments[i].get('body'))
