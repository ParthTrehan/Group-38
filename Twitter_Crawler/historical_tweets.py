import json
import tweepy
import time
import os
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API
import couchdb
import sys
import pprint
from better_profanity import profanity
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def add_tweet(tweet_data):
    #print("Stop 2")
    tweet_doc_id = tweet_data["id_str"]
    tweet_lang = tweet_data["lang"]
    tweet_text = tweet_data["text"]
    tweet_coords = tweet_data["coordinates"]
    tweet_user_id = tweet_data["user"]["screen_name"]
    tweet_dow = tweet_data["created_at"].split()[0]

    if tweet_lang == "en" and tweet_coords is not None:
        #print(tweet_coords)
        #print("Stop 3")
        if tweet_coords["coordinates"][0] >= 144.43 and tweet_coords["coordinates"][0] <= 145.41 and tweet_coords["coordinates"][1] >= -38.53 and tweet_coords["coordinates"][1] <= -37.40:
            #Classifying tweets based on keywords
            #print("Stop 4")
            if profanity.contains_profanity(tweet_text) or any(i.lower() in tweet_text.lower() for i in lust_words):
                lust_metric = 1
            else:
                lust_metric = 0
            #End of classification
            #print("Stop 5")
            point = Point(tweet_coords["coordinates"][0], tweet_coords["coordinates"][1])
            tweet_lga = "Not Found"
            for lga_name, coords in polygon_dict.items():
                if coords.contains(point):
                    tweet_lga = lga_name
            #print(tweet_lga)
            doc = {"_id" : tweet_doc_id, "user_name" : tweet_user_id, "day_of_week" : tweet_dow, "text" : tweet_text, "coordinates" : tweet_coords["coordinates"], "lga_name" : tweet_lga, "lust_metric" : lust_metric}
            #print("Stop 6")
            try:
                #print("Stop1")    
                tweets_db.save(doc)
                print('Tweet added: ' + tweet_doc_id)
                #print("Stop 7")
            except couchdb.http.ResourceConflict as e:
                print("Stop7 Error : ", e)
                pass
    else:
        pass

pp = pprint.PrettyPrinter(indent=2)
input_file = "melb_tweets_2017.tweet"

with open('lust_words.json') as lust_data:
    lust_data = json.load(lust_data)
with open('final_28_grids.json') as final_data:
    finaljson = json.load(final_data)

polygon_dict = {}
lust_words = lust_data["lust_words"]

count = 0

for element in finaljson['data']:
    coordinate_set = np.array(element['geometry']['coordinates'][0][0])
    polygon_dict[element["properties"]["vic_lga__2"]] = Polygon(coordinate_set)

config = json.load(open('config.json'))
data = json.load(open('db_config.json'))
server_address = data["db_url"]
tweets_db_name = data["tweets_db_name"]
users_db_name = data["users_db_name"]
couch = couchdb.Server(server_address)

try:
    tweets_db = couch[tweets_db_name]
except:
    tweets_db = couch.create(tweets_db_name)

try:
    users_db = couch[users_db_name]
except:
    users_db = couch.create(users_db_name)

with open("melb_tweets_2017.tweet", 'rt', encoding='utf8') as f:
#print("stop 2")
    cnt = 0
    for line in f:
#print("stop 3", i) 
# #to divide twitter data file
        try: #some json lines (like line 1) don't contain tweets and throw error when loading
    #print(i, rank)
            tweet = line[:len(line) - 2]
            tweet = json.loads(tweet)
            #print(cnt + 1,"*****", tweet)
            #print("Stop 1******", cnt+1)
            #pp.pprint(tweet['doc'])
            tweet_data = tweet['doc']
            add_tweet(tweet_data)            
            #cnt +=1
        #print("Stop 2")
        except BaseException as e:
            print("Error: ", e)
                #cnt += 1
            #if cnt > 5:
            #    break