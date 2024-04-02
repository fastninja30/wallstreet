import requests
import json

with open('../Credentials.json', 'r') as file:
    credentials = json.load(file)

reddit_creds = credentials['reddit_api']['3']

# Setting up authorization header
ID = reddit_creds['id']
SECRIT_KEY = reddit_creds['SECRET_KEY']
auth = requests.auth.HTTPBasicAuth(ID, SECRIT_KEY)


# https://www.reddit.com/prefs/apps
# https://old.reddit.com/prefs/apps/
data = {
    'grant_type': 'password',
    'username': reddit_creds['username'],
    'password' : reddit_creds['password']
}

headers = {'User-Agent': "WallStreetPulse/0.0.1"}
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']

headers['Authorization'] = f'bearer {TOKEN}'


# Request using API
# API can be found https://www.reddit.com/dev/api/
BASE_URL = 'https://oauth.reddit.com'

def get_hot_posts():
    return requests.get( BASE_URL + "/r/wallstreetbets/hot", headers=headers)

# ADD MORE USEFUL API HERE
