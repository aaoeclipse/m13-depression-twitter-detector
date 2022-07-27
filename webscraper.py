from enum import Enum
import tweepy
import pandas as pd
from dotenv import load_dotenv
import os

class Status(Enum):
    SUCCESS = 1
    FAIL = 0

def tweet_valid(t):
    no_image = 'media' not in t.entities
    not_retweeted = not t.text.startswith("RT @") 
    not_mention= not t.text.startswith("@") 
    english_tweet = t.lang == 'en'
    return no_image and not_retweeted and english_tweet and not_mention

class TwitterBot():
    def __init__(self, path=".env") -> None: 
        self.env_path = path
        self.API = self.initialize()


    def initialize(self): # Authenticate to Twitter
        load_dotenv(self.env_path)
        AK = os.environ.get("API_KEY")
        ASK = os.environ.get("API_SECRET_KEY")
        AT = os.environ.get("ACCESS_TOKEN")
        AST = os.environ.get("ACCESS_SECRET_TOKEN")
        auth = tweepy.OAuthHandler(AK, ASK)
        auth.set_access_token(AT, AST)
        return tweepy.API(auth)    # Create API object


    def is_connected(self):
        try:
            self.API.verify_credentials()
            return True
        except:
            return False

    
    def get_user(self, user_id):
        status = Status.FAIL
        df = pd.DataFrame(columns=["userID", "tweet", "lang", "timestamp", "favorite_count"])
        try:
            tweets = self.API.user_timeline(screen_name=user_id, count=500)
            counter = 0
            for tweet in tweets:
                if counter == 20:
                    status = Status.SUCCESS
                    break
                elif tweet_valid(tweet):
                    row = {"userID" : user_id, "tweet":tweet.text, "lang":tweet.lang, "timestamp":tweet.created_at, "favorite_count":tweet.favorite_count, "retweet_count" : tweet.retweet_count}
                    df = pd.concat([df, pd.DataFrame(data=row, index=[0])], ignore_index=True)
                    counter += 1
        finally:
            return (status, df)


if __name__ == "__main__":
    bot = TwitterBot()
    state, df = bot.get_user("VancityReynolds")
    print(state)
    print(df.head(20))