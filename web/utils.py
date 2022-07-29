

# Packages
import pandas as pd
import ast

# Local Packages
from scrapper.webscraper import Status, TwitterBot
import metrics.metrics as metrics
import sentimental.sentimental_model as sent_model
import model.ml_model as model


bot = TwitterBot()


def get_twitter(twitter: str) -> str:
    """ transform twitter to the correct format

    Args:
        twitter (str): twitter handler

    Returns:
        str: twitter handler with correct format.
    """

    return twitter.strip("@")


def fetch_tweets(twitter: str) -> pd.DataFrame:
    """retrieve the last 50 tweets from the twitter handler

    Args:
        twitter (str): twitter handler

    Returns:
        list: list of twitters of the user
    """
    state, df = bot.get_user(twitter)

    if state == Status.FAIL:
        raise Exception("Failed to get twitters")

    return df


def get_tweeters_with_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """generate metrics per tweets

    Args:
        tweets (df): df of tweets

    Returns:
        list: list of metrics of each tweet
    """
    df['tweet_vector'] = df['tweet'].apply(metrics.get_tweet_vector)
    df['sentimental_value'] = sent_model.get_sentimental(df)
    df['tweet_vector'] = df.apply(lambda x: metrics.get_tweet_data_vector(x.tweet_vector, x.timestamp, x.favorite_count, x.retweet_count, x.sentimental_value), axis=1)
    df['tweet_vector'] = df.apply(lambda x: ast.literal_eval(str(x.tweet_vector)), axis='columns')
    df = df.join(df['tweet_vector'].apply(pd.Series))
    df = pd.DataFrame(df.groupby('userID').mean())
    return df





def predict_model_with_array(df: pd.DataFrame) -> float:
    """predict with model the depression level of the list of df

    Args:
        df (list): list of df

    Returns:
        float: from 0 to 1 the prob of being depressed
    """
    return model.predict(df)


def full_process(twitter: str) -> float:
    """full pipeline of the model

    Args:
        twitter (str): twitter account

    Returns:
        float: probability of it being with depression
    """   
    tweets = fetch_tweets(get_twitter(twitter))
    tweets_w_metrics = get_tweeters_with_metrics(tweets)
    return predict_model_with_array(tweets_w_metrics) * 15