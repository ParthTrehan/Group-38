import couchdb
import json
data = json.load(open('all_tweets.json'))
config = json.load(open('/home/ubuntu/deploy/Twitter_Crawler/db_config.json'))
tweets = data["rows"]
server_address = config["db_url"]
tweets_db_name = config["tweets_db_name"]
users_db_name = config["users_db_name"]
couch = couchdb.Server(server_address)
try:
    tweets_db = couch[tweets_db_name]
except:
    tweets_db = couch.create(tweets_db_name)

for tweet in tweets:
    tweets_db.save(tweet["doc"])