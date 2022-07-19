import tweepy
import pandas as pd
import json
from dotenv import load_dotenv
import os


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


userid = "Crissy"
tweets = api.user_timeline(screen_name=userid, count=500)
df = pd.DataFrame(columns=["userID", "tweet", "lang", "timestamp", "favorite_count"])
counter = 0
for tweet in tweets:
    if counter == 20:
        df.to_csv(f"{userid}_tweets.csv", index=False)
        break
    elif tweet_valid(tweet):
        row = {"userID" : userid, "tweet":tweet.text, "lang":tweet.lang, "timestamp":tweet.created_at, "favorite_count":tweet.favorite_count, "retweet_count" : tweet.retweet_count}
        df = pd.concat([df, pd.DataFrame(data=row, index=[0])], ignore_index=True)
        counter += 1
        print(tweet.text)
        

print(f"user {userid} had {counter} tweets saved") 


