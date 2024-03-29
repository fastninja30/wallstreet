import reddit_api
import gpt_api
import json

# Sample usages
posts = reddit_api.get_hot_posts()

json_object=json.dumps(posts.json())
# print(type(json_object))
with open("sample.json", "w") as outfile:
    outfile.write(json_object)
data=json.loads(json_object)
print(data['data']['dist'])
titles=[data['data']['children'][i]['data']['title'] for i in range(0,len(data['data']['children']))]
numOfComments=[data['data']['children'][i]['data']['num_comments'] for i in range(0,len(data['data']['children']))]
titles_numComments=[(data['data']['children'][i]['data']['title'],data['data']['children'][i]['data']['num_comments']) for i in range(0,len(data['data']['children']))]
print(titles_numComments)
# response, chat_history = gpt_api.get_response("What is RCOS")

# response, chat_history = gpt_api.get_response("What is WallStreetPulse")








