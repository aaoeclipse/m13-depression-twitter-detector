import tweepy
import pandas as pd
import json
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv(".env")
AK = os.environ.get("API_KEY")
ASK = os.environ.get("API_SECRET_KEY")
AT = os.environ.get("ACCESS_TOKEN")
AST = os.environ.get("ACCESS_SECRET_TOKEN")

def initialize(): # Authenticate to Twitter
    auth = tweepy.OAuthHandler(AK, ASK)
    auth.set_access_token(AT, AST)
    return tweepy.API(auth)    # Create API object


def check_connection(API):
    try:
        API.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

def tweet_valid(t):
    no_image = 'media' not in t.entities
    not_retweeted = not t.text.startswith("RT @") 
    not_mention= not t.text.startswith("@") 
    english_tweet = t.lang == 'en'
    return no_image and not_retweeted and english_tweet and not_mention

api = initialize()
check_connection(api)

df = pd.DataFrame(columns=["userID", "tweet", "lang", "timestamp", "favorite_count", "retweet_count"])
num_users = 0

list_of_userids =pd.read_csv("user_ids.csv")['screenName']

for ind, userid in enumerate(list_of_userids):
    print(f"Now working on user {userid} which is ordered {ind} on the list")
    try:
        tweets = api.user_timeline(screen_name=userid, count=500)
        userid_list, tweet_list, lang_list, timestamp_list, favorite_count_list, retweet_count_list, = [], [], [], [], [], []
        for tweet in tweets:
            if len(userid_list) == 20:
                user_tweets = {"userID" : userid_list, "tweet":tweet_list, "lang":lang_list, "timestamp":timestamp_list, "favorite_count":favorite_count_list, "retweet_count" : retweet_count_list}
                df = pd.concat([df, pd.DataFrame(data=user_tweets)], ignore_index=True)
                print(f"User {userid} was scraped\n The number of users is now{num_users}")
                num_users += 1
                break
            elif tweet_valid(tweet):
                userid_list.append(userid)
                tweet_list.append(tweet.text)
                lang_list.append(tweet.lang)
                timestamp_list.append(tweet.created_at)
                favorite_count_list.append(tweet.favorite_count)
                retweet_count_list.append(tweet.retweet_count)
    except:
        print(f"Failed to get user {userid}")
    
    
    if (ind + 1) % 1450 == 0:
        df.to_csv(f"tweets_at_ind_{ind}.csv")
        sleep(60 * 15)

    df.to_csv(f"all_tweets.csv", index=False)
    print(f"The table contains {num_users} users tweets") 


