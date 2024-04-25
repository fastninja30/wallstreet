import requests
# Setting up authorization header
ID = "mGJKXOitGGulU5pBJ9Zmqg"
SECRET_KEY = "zZR3V_O4kRdzjJqKZN9-oNluADiHfg"
auth = requests.auth.HTTPBasicAuth(ID, SECRET_KEY)

with open('pswd.txt', 'r') as f:
    pswd = f.read()

data = {
    'grant_type': 'password',
    'username': 'WallStreetPulse',
    'password' : pswd
}

headers = {'User-Agent': "WallStreetPulse/0.0.1"}
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'
BASE_URL = 'https://oauth.reddit.com/r/wallstreetbets'

class Reddit_API:
    def __init__(self):
        self.client_id = ID
        self.secret_key = SECRET_KEY
        self.auth = auth
        self.data = data
        self.headers = headers
        self.token = TOKEN

    # Returns a list sorted posts
    # Sort by new, hot, top, controversial, rising, best
    def get_sorted_posts(self, sort, limit):
        return requests.get(BASE_URL + "/" + sort + "?limit=" + limit, headers=headers).json()

    # Returns the post id of a post
    # post should be in this format json.get('data').get('children')[i]
    def get_post_id(self, post):
        return post.get('data').get('id')

    # Returns a list of data based on id of the post
    # post[0] contains the post content
    # post[1] contains the post comments
    def get_post_data(self, id, limit):
        return requests.get(BASE_URL + "/comments/" + id + "?limit=" + limit, headers=headers).json()


    # Instructions on how to access data
    # After creating the dictionaries
    # To access the data of a post, use .get('{key}') for an element in the list

    # KEYS FOR POST
    # 'approved_at_utc', 'subreddit', 'selftext', 'user_reports', 'saved', 'mod_reason_title', 'gilded', 'clicked',
    # 'title', 'link_flair_richtext', 'subreddit_name_prefixed', 'hidden', 'pwls', 'link_flair_css_class', 'downs',
    # 'thumbnail_height', 'top_awarded_type', 'parent_whitelist_status', 'hide_score', 'name', 'quarantine',
    # 'link_flair_text_color', 'upvote_ratio', 'author_flair_background_color', 'ups', 'domain', 'media_embed',
    # 'thumbnail_width', 'author_flair_template_id', 'is_original_content', 'author_fullname', 'secure_media',
    # 'is_reddit_media_domain', 'is_meta', 'category', 'secure_media_embed', 'link_flair_text', 'can_mod_post',
    # 'score', 'approved_by', 'is_created_from_ads_ui', 'author_premium', 'thumbnail', 'edited',
    # 'author_flair_css_class', 'author_flair_richtext', 'gildings', 'post_hint', 'content_categories', 'is_self',
    # 'subreddit_type', 'created', 'link_flair_type', 'wls', 'removed_by_category', 'banned_by', 'author_flair_type',
    # 'total_awards_received', 'allow_live_comments', 'selftext_html', 'likes', 'suggested_sort', 'banned_at_utc',
    # 'url_overridden_by_dest', 'view_count', 'archived', 'no_follow', 'is_crosspostable', 'pinned', 'over_18',
    # 'preview', 'all_awardings', 'awarders', 'media_only', 'link_flair_template_id', 'can_gild', 'spoiler',
    # 'locked', 'author_flair_text', 'treatment_tags', 'visited', 'removed_by', 'mod_note', 'distinguished',
    # 'subreddit_id', 'author_is_blocked', 'mod_reason_by', 'num_reports', 'removal_reason',
    # 'link_flair_background_color', 'id', 'is_robot_indexable', 'num_duplicates', 'report_reasons', 'author',
    # 'discussion_type', 'num_comments', 'send_replies', 'media', 'contest_mode', 'author_patreon_flair',
    # 'author_flair_text_color', 'permalink', 'whitelist_status', 'stickied', 'url', 'subreddit_subscribers',
    # 'created_utc', 'num_crossposts', 'mod_reports', 'is_video'

    # Returns a dictionary of post data
    # Use post[0]
    def get_post_dict(self,post):
        return post.get('data').get('children')[0].get('data')

    # KEYS FOR COMMENTS
    # 'subreddit_id', 'approved_at_utc', 'author_is_blocked', 'comment_type', 'awarders', 'mod_reason_by',
    # 'banned_by', 'author_flair_type', 'total_awards_received', 'subreddit', 'author_flair_template_id',
    # 'likes', 'replies', 'user_reports', 'saved', 'id', 'banned_at_utc', 'mod_reason_title', 'gilded',
    # 'archived', 'collapsed_reason_code', 'no_follow', 'author', 'can_mod_post', 'created_utc',
    # 'send_replies', 'parent_id', 'score', 'author_fullname', 'removal_reason', 'approved_by', 'mod_note',
    # 'all_awardings', 'body', 'edited', 'top_awarded_type', 'author_flair_css_class', 'name', 'is_submitter',
    # 'downs', 'author_flair_richtext', 'author_patreon_flair', 'body_html', 'gildings', 'collapsed_reason',
    # 'distinguished', 'associated_award', 'stickied', 'author_premium', 'can_gild', 'link_id',
    # 'unrepliable_reason', 'author_flair_text_color', 'score_hidden', 'permalink', 'subreddit_type', 'locked',
    # 'report_reasons', 'created', 'author_flair_text', 'treatment_tags', 'collapsed',
    # 'subreddit_name_prefixed', 'controversiality', 'depth', 'author_flair_background_color',
    # 'collapsed_because_crowd_control', 'mod_reports', 'num_reports', 'ups'

    # Get replies collapsed in a thread (Needs work)
    def _get_thread_dict(self, dicts, post_id, depth, comment_id):
        thread = requests.get(BASE_URL + "/comments/" + post_id + "/comment/" + comment_id[3:] + "/",headers=headers).json()
        if isinstance(thread[1].get('data').get('children')[0].get('replies'), dict):
            print(thread[1].get('data').get('children')[0].get('data').get('replies'))
            self.get_dicts(thread[1].get('data').get('children')[0], dicts, post_id, depth)

    # Gets the dictionaries of hidden replies and adds them to the list of dicts
    def _get_more_dicts(self, comment, dicts, post_id, depth):
        children = ""
        children_size = len(comment.get('data').get('children'))
        for i in range(0, children_size):
            if i == children_size - 1:
                children += comment.get('data').get('children')[i]
            else:
                children += comment.get('data').get('children')[i] + ","

        # API request to get hidden replies
        replies = requests.get(BASE_URL + "/api/morechildren?link_id=t3_" + post_id + "&limit_children=false&depth=" + depth + "&children=" + children,headers=headers).json()
        if replies.get('jquery')[10][3][0]:
            reply_count = len(replies.get('jquery')[10][3][0])
            for i in range(0, reply_count):
                if replies.get('jquery')[10][3][0][i].get('data').get('body'):
                    dicts.append(replies.get('jquery')[10][3][0][i].get('data'))
                # else:
                #     comment_id = f"{replies.get('jquery')[10][3][0][i].get('data').get('parent_id')}"
                #     self.get_thread_dict(dicts, post_id, depth, comment_id)

    # Returns a list of dictionaries
    def get_dicts(self, data, dicts, id, depth):
        size = len(data.get('data').get('children'))
        for i in range(0, size):
            # Check if the reply has any content
            if not data.get('data').get('children')[i].get('data').get('body'):
                self._get_more_dicts(data.get('data').get('children')[i], dicts, id, depth)
            else:
                dicts.append(data.get('data').get('children')[i].get('data'))
            # Get the replies to the comment
            if isinstance(data.get('data').get('children')[i].get('data').get('replies'), dict):
                self.get_dicts(data.get('data').get('children')[i].get('data').get('replies'), dicts, id, depth)