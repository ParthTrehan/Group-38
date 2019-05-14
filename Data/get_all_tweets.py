import couchdb
import json

config = json.load(open('../Twitter_Crawler/db_config.json'))
server_address = config["db_url"]
tweets_db_name = "mcbc"
couch = couchdb.Server(server_address)

try:
    tweets_db = couch[tweets_db_name]
except:
    tweets_db = couch.create(tweets_db_name)
with open("all_tweets.json", encoding='utf8') as f:
        #print(line)
        tweets = json.load(f)
        tweets = tweets["rows"]
        for tweet in tweets:
            single = tweet["doc"]
            