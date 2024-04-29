
# https://developers.google.com/custom-search/v1/overview
# search engine id: b3dc3b1ce374e440c
# api key: AIzaSyBG2uCYJDwpZLlVcsmracUk3zRSJZMpn98
import requests
from datetime import datetime
import json
import os
import random

# Define the base URL for the Custom Search JSON API
base_url = "https://www.googleapis.com/customsearch/v1"

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
CSE_list = credentials['custom_search_engine']
CSE_keys = list(credentials['custom_search_engine'].keys())
CSE = credentials['custom_search_engine'][random.choice(CSE_keys)]


# start_date = "20210101"
# end_date = "20210228"

# params
#   start_date: string with format %Y%m%d
#   end_date: string with format %Y%m%d
# returns
# a list of all article id during the given time period
def search_by_time_period(start_date = "20231203", end_date = "20240110"):
    article_ids = []
    num = 10
    while(int(start_date) < int(end_date) and num == 10):
        CSE = credentials['custom_search_engine'][random.choice(CSE_keys)]
        print(f'Request from Google: {start_date} {end_date}')
        params = {
            "key": CSE['api_key'], # The API key
            "cx": CSE["CSE_id"], # The CSE ID
            "q": "reddit", # The search query
            "sort": f"date:r:{start_date}:{end_date}", # The date range filter
            "num": 10 # The number of results to return
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(data)
            num = len(data["items"])
            for item in data["items"]:
                article_ids.append(item['link'].split('/')[-3])
                date_obj = datetime.strptime(item['snippet'][:12].lstrip().rstrip(), "%b %d, %Y")
                start_date = max(date_obj.strftime("%Y%m%d"),start_date)
        else:
            print(f"Request failed with status code {response.status_code}")
    print("Finished all requests")
    return article_ids

def search(start_date = "20231203", end_date = "20240110"):
    data_list = []
    num = 10
    thres  = 5
    i = 0
    while(int(start_date) < int(end_date) and num == 10 and i < thres):
        i += 1
        CSE = credentials['custom_search_engine'][random.choice(CSE_keys)]
        print(f'Request from Google: {start_date} {end_date}')
        params = {
            "key": CSE['api_key'], # The API key
            "cx": CSE["CSE_id"], # The CSE IDs
            "q": "reddit", # The search query
            "sort": f"date:r:{start_date}:{end_date}", # The date range filter
            "num": 10 # The number of results to return
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            num = len(data["items"])
            data_list.append(data)
            for item in data["items"]:
                date_obj = datetime.strptime(item['snippet'][:12].lstrip().rstrip(), "%b %d, %Y")
                start_date = max(date_obj.strftime("%Y%m%d"),start_date)
        else:
            print(f"Request failed with status code {response.status_code}")

    if i == thres:
        print("exceed maximum retries")
    print("Finished all requests")
    return data_list



if __name__ == "__main__":
    print(search())