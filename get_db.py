from redditData.google_search import search_by_time_period
from redditData.reddit_api import Reddit_API
import SQLjsonHelper

def get_post_info(start_date = "20231203", end_date = "20240110"):
    article_ids=search_by_time_period(start_date,end_date)
    print(article_ids)
    api=Reddit_API()

    for id in article_ids:
        data=api.get_post_data(id,"1000")
        # print(api.get_post_dict(data[0]))
        SQLjsonHelper.display_table()
        # dict={}
        # api.get_dicts(data[0],dict,id,10)
        # print(dict)
if __name__ == "__main__":
    get_post_info()
