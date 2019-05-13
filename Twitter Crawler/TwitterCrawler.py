#Code for harvesting tweets
""" Logic for Harvesting:
    1. Get token from config.json file with location coordinates for melbourne
    2. Try to get tweets based on location provided using stream API. If an error is thrown, then go to 6.
    3. Store tweet in couchdb tweets DB using id_str as primary key (will throw conflict if same tweet already exists). When a tweet is stored, it is assigned a lust metric, a day of the week label and LGA zone name where the coordinates of the tweets lie.
    4. Get user_id from tweet and try to add user_id to couchdb users DB (will throw conflict if user has already been added)
    5. If no conflict is thrown, then use search API to get user's historical 3200 tweets using user_timeline and add them to the tweets DB following same rules as 3.
    6. Get the next token from config.json and try harvesting
"""
import json
import tweepy
import time
import random
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API
import couchdb
import sys
from better_profanity import profanity
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#Global Variables
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


#Functions
def add_tweet(tweet_data):
    tweet_doc_id = tweet_data["id_str"]
    tweet_lang = tweet_data["lang"]
    tweet_text = tweet_data["text"]
    tweet_coords = tweet_data["coordinates"]
    tweet_user_id = tweet_data["user"]["screen_name"]
    tweet_dow = tweet_data["created_at"].split()[0]

    if tweet_lang == "en" and tweet_coords is not None:
        #print(tweet_coords)
        if tweet_coords["coordinates"][0] >= 144.43 and tweet_coords["coordinates"][0] <= 145.41 and tweet_coords["coordinates"][1] >= -38.53 and tweet_coords["coordinates"][1] <= -37.40:
            #Classifying tweets based on keywords
            if profanity.contains_profanity(tweet_text) or any(i.lower() in tweet_text.lower() for i in lust_words):
                lust_metric = 1
            else:
                lust_metric = 0
            #End of classification
            point = Point(tweet_coords["coordinates"][0], tweet_coords["coordinates"][1])
            tweet_lga = "Not Found"
            for lga_name, coords in polygon_dict.items():
                if coords.contains(point):
                    tweet_lga = lga_name
            #print(tweet_lga)
            doc = {"_id" : tweet_doc_id, "user_name" : tweet_user_id, "day_of_week" : tweet_dow, "text" : tweet_text, "coordinates" : tweet_coords["coordinates"], "lga_name" : tweet_lga, "lust_metric" : lust_metric}
            try:
                #print("Stop1")    
                tweets_db.save(doc)
                print('Tweet added: ' + tweet_doc_id)
                global count
                count = 0
            except couchdb.http.ResourceConflict:
                #print("Stop2")
                pass
    else:
        pass
#Classes
class listener(tweepy.StreamListener):

    def on_data(self, data):

        try:
            #print("Stop1")
            tweet_data = json.loads(data)
            add_tweet(tweet_data)
            user_name = tweet_data["user"]["screen_name"]
            user_id = tweet_data["user"]["id_str"]
            tweet_coords = tweet_data["coordinates"]
            doc = {"_id" : user_id, "coords" : tweet_coords}
            #print("Stop2")
            try:
                users_db.save(doc)
                #print("stop3")
                print("Adding user to couchdb:", user_id)
                if tweet_coords is not None:
                    #print("stop4")    
                    for doc in tweepy.Cursor(api.user_timeline, id=user_name).items(3200):
                        raw_tweet = json.dumps(doc._json)
                        tweet = json.loads(raw_tweet)
                        add_tweet(tweet)
                    return True
                else:
                    return True
            except couchdb.http.ResourceConflict:
                return True
        
        except BaseException as e:
            print("Error:", e)
            return True

    def on_error(self, status):
        if status == 420:
            print(status)
            return False

#load the configuration file and database
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

#Main Loop
while True:
    id = random.choice(list(config))
    value = config[id]
    consumer_key = value["consumer_key"]
    consumer_secret = value["consumer_secret"]
    access_token_key = value["access_token_key"]
    access_token_secret = value["access_token_secret"]
    locations = value['locations']
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = API(auth)
    #print("Stop 1")
    try:
        stream = Stream(auth, listener())
        print("Harvester started using id : ", id)
        stream.filter(locations = locations)
    except Exception as e:
        count += 1
        print(e)
        print("Will try harvesting using next API tokens in 5 secs")
        time.sleep(5)
        stream.disconnect()
    if count == len(config):
        print("All tokens are exhausted and are getting timeout from twitter server. Waiting for 15 mins...")
        time.sleep(15*60)