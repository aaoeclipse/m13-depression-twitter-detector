from keras.models import load_model
from keras.preprocessing.text import Tokenizer
import keras
import numpy as np
import nltk
import pickle

import pandas as pd
from tqdm import tqdm
# from tqdm.auto import tqdm  # for notebooks

# Create new `pandas` methods which use `tqdm` progress
# (can use tqdm_gui, optional kwargs, etc.)
tqdm.pandas()

max_tweet_length = 100

#Tokenizer
number_of_words = 10000
nltk.download('stopwords')


# tokenizer = Tokenizer(num_words = number_of_words)

with open('web/model/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


from keras.utils import pad_sequences

def get_sentimental(df_given: pd.DataFrame) -> pd.Series:
    df = df_given.copy()

    model = load_model('web/model/saved_model.h5')

    df['Clean_TweetText'] = df['tweet'].str.replace("@", "") 
    # Removing links
    df['Clean_TweetText'] = df['tweet'].str.replace(r"http\S+", "") 
    # Removing Punctuations, Numbers, and Special Characters
    df['Clean_TweetText'] = df['tweet'].str.replace("[^a-zA-Z]", " ") 
    # Remove stop words
    stopwords=nltk.corpus.stopwords.words('english')
    def remove_stopwords(text):
        clean_text=' '.join([word for word in text.split() if word not in stopwords])
        return clean_text
    df['Clean_TweetText'] = df['Clean_TweetText'].apply(lambda text : remove_stopwords(str(text).lower()))
    def pre_process(tweet):
        my_tokenized_tweet = tokenizer.texts_to_sequences([tweet])

        my_tokenized_tweet = pad_sequences(my_tokenized_tweet, 
                                                            maxlen = max_tweet_length)
        return my_tokenized_tweet

    df["processed_tweets"] = df.progress_apply(lambda row: pre_process(row["Clean_TweetText"]) , axis =1 )

    # df['Clean_TweetText'] = df['tweet'].str.replace("@", "") 
    
    x = np.zeros((len(df), 100))
    for i in range(len(df)):
        x[i,:]= df["processed_tweets"].values[i]

    result = model.predict(x)
    return pd.Series(result.T[0])