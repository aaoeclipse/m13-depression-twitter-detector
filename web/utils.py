
def get_twitter(twitter: str) -> str:
    """ transform twitter to the correct format

    Args:
        twitter (str): twitter handler

    Returns:
        str: twitter handler with correct format
    """
    pass


def fetch_tweets(twitter: str) -> list:
    """retrieve the last 50 tweets from the twitter handler

    Args:
        twitter (str): twitter handler

    Returns:
        list: list of twitters of the user
    """
    pass


def get_tweeters_with_metrics(tweets: list) -> list:
    """generate metrics per tweets

    Args:
        tweets (list): list of tweeters

    Returns:
        list: list of metrics of each tweet
    """
    pass


def predict_model_with_array(metrics: list) -> float:
    """predict with model the depression level of the list of metrics

    Args:
        metrics (list): list of metrics

    Returns:
        float: from 0 to 1 the prob of being depressed
    """
    pass
