import tweepy
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

check_connection(initialize())