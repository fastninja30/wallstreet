from redditData.google_search import *
from datetime import datetime
from localDatabase.SQL import *

SQL = SQL("lateGME.db")
'''
data = SQL.search("google_search", order_by="Created_date DESC", limit=1)[0]
if len(data) != 0:
    start_date = data['Created_date']
    start_date = datetime.utcfromtimestamp(int(start_date) / 1000.0)
    start_date = start_date.strftime('%Y%m%d')
else:
    start_date = "20210101"
end_date = "20210228"
'''
start_date = "20210228"
end_date = "20211030"

data_list = search(start_date, end_date)
print(data_list)

for result in data_list:
    for data in reversed(result["items"]):
        try:
            # skip unwanted search result
            if 'og:description' not in data['pagemap']['metatags'][0]:
                continue
            # Extracting required information
            id = data['link'].split('/')[-3]
            title = data['title']
            URL = data['link']

            created_date = data['snippet'].split()[0:3]
            created_date = " ".join(created_date).replace(',', '')
            created_date = datetime.strptime(created_date, "%b %d %Y")
            created_date = int(created_date.timestamp() * 1000)
            created_date = datetime.utcfromtimestamp(created_date / 1000.0)
            created_date = created_date.strftime('%Y%m%d')


            poster_name = data['pagemap']['metatags'][0]['og:description'].split()[2]
            votes = data['pagemap']['metatags'][0]['og:description'].split()[4]
            comments = data['pagemap']['metatags'][0]['og:description'].split()[7]

            post_info = {
                "id": id,
                "title": title,
                "URL": URL,
                "created_date": created_date,
                "author": poster_name,
                "votes": votes,
                "num_comments": comments,
                "is_visited": "False"
            }
            SQL.insert("google_search", post_info)
        except:
            pass

SQL.print_table("google_search")
