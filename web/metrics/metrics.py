import datetime
import ast
import nltk
import re
from nltk.tokenize import sent_tokenize
import string
from nltk.stem import WordNetLemmatizer
import csv
from textblob import TextBlob
import re
import pandas as pd

EnglishShortened_path = 'model/content/EnglishShortened.csv'

sentimental_depressed_path = 'model/content/sentimental_depressed.csv'
sentimental_non_depressed_path = 'model/content/sentimental_non_depressed.csv'

non_depressed_tweets_path = 'model/content/non_depressed_tweets.csv'
depressed_tweets_path = 'model/content/depressed_tweets.csv'

def clean_tweet(tweet):
  tweet = re.sub(r"\d+", "", tweet)
  
  tweet = tweet.replace(".", "")
  tweet = tweet.replace("(", "")
  tweet = tweet.replace(")", "")
  tweet = tweet.replace("'m", " am")
  tweet = tweet.replace("'s", " is")
  tweet = tweet.replace("'ve", " have")
  tweet = tweet.replace("n't", " not")
  tweet = tweet.replace("'re", " are")
  tweet = tweet.replace("'d", " would")
  tweet = tweet.replace("'ll", " will")
  tweet = tweet.replace("\r", " ")
  tweet = tweet.replace("\n", " ")
  tweet = tweet.strip().lower()
  
  tweet = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", tweet)
  return tweet

def find_words_frequency(tweet, words_dict):
  tweet_clean = clean_tweet(tweet)
  token = re.findall('\w+', tweet_clean)
  words_freq = nltk.FreqDist(token)
  total_freq = 0
  for item in words_dict:
    item_freq = words_freq.freq(item)
    total_freq += item_freq
  return total_freq 

def absolutist_words_metric(tweet):
  tweet_clean = clean_tweet(tweet)
  absolutist_words_dict = ["absolutely", "all", "always", "complete", "completely", "constant", "constantly", "definitely", "entire",
                           "ever", "every", "everyone", "everything", "full", "must", "never", "nothing", "totally", "whole"]
  return find_words_frequency(tweet_clean, absolutist_words_dict)

def first_pronouns_metric(tweet):
  tweet_clean = clean_tweet(tweet)
  first_person_pronoun_dict = ["i", "me", "my", "mine", "we", "us", "our", "ours"]
  return find_words_frequency(tweet_clean, first_person_pronoun_dict)

def second_third_pronouns_metric(tweet):
  tweet_clean = clean_tweet(tweet)
  second_third_person_pronoun_dict = ["you", "your", "yours",
                                      "he", "she", "it", "him", "her", "his", "its", "hers",
                                      "they", "them", "their", "theirs"]
  return find_words_frequency(tweet_clean, second_third_person_pronoun_dict)

def TextBlob_metrics(tweet):
  tweet_clean = clean_tweet(tweet)
  blob = TextBlob(tweet_clean)
  for sentence in blob.sentences:
    polarity = sentence.sentiment.polarity
    subjectivity = sentence.sentiment.subjectivity
  return polarity, subjectivity

def create_anew_dict():
  anew_dict = {}
  with open(EnglishShortened_path, mode='r') as infile:
    reader = csv.reader(infile)
    anew_dict = {rows[0]:[rows[1], rows[2], rows[3]] for rows in reader}
  return anew_dict


def lemmatize_tweet(tweet_clean):
  token = re.findall('\w+', tweet_clean)
  lemmatized_words = []
  lemmatizer = WordNetLemmatizer()
  for word in token:
    lemmatized_words.append(lemmatizer.lemmatize(word))
  return lemmatized_words

def anew_metric(tweet):
  anew_dict = create_anew_dict()
  valence, arousal, dominance = 0, 0, 0
   
  tweet_clean = clean_tweet(tweet)
  tweet_words = lemmatize_tweet(tweet_clean)
  N_words_total  = len(tweet_words) 
   
  for index in range(N_words_total):
    # check for negation in 3 words before current word
    j = index-1
    neg = False
    while j >= 0 and j >= index-3:
      if tweet_words[j] == 'not' or tweet_words[j] == 'no':
        neg = True
        break
      j -= 1

    # search for lemmatized word in ANEW
    if tweet_words[index] in anew_dict.keys():
      if neg:
        valence += float(anew_dict[tweet_words[index]][0])
        arousal += float(anew_dict[tweet_words[index]][1])
        dominance +=  float(anew_dict[tweet_words[index]][2])
      else:
        valence += (10 - float(anew_dict[tweet_words[index]][0]))
        arousal += (10 - float(anew_dict[tweet_words[index]][1]))
        dominance += (10 - float(anew_dict[tweet_words[index]][2]))

  if N_words_total == 0:
    return 0, 0, 0
  else:
    return valence/N_words_total, arousal/N_words_total, dominance/N_words_total

def pronominalisation_index(tweet):
  tweet_clean = clean_tweet(tweet)
  tokens = re.findall('\w+', tweet_clean)
  tags = nltk.pos_tag(tokens, tagset='universal')
  tags_freq = nltk.FreqDist(tag for (word, tag) in tags)
  if tags_freq['NOUN'] == 0:
    return 0
  else:
    return tags_freq['PRON']/tags_freq['NOUN']

def readiness_to_action_index(tweet):
  tweet_clean = clean_tweet(tweet)
  tokens = re.findall('\w+', tweet_clean)
  tags = nltk.pos_tag(tokens, tagset='universal')
  tags_freq = nltk.FreqDist(tag for (word, tag) in tags)
  if tags_freq['NOUN'] == 0:
    return 0
  else:
    return tags_freq["VERB"]/tags_freq["NOUN"]



def punctuation_metric(tweet):
  count = lambda l1,l2: sum([1 for x in l1 if x in l2])
  num_punct = count(tweet,set(string.punctuation))          
  num_sentences = len(sent_tokenize(tweet))
  if num_sentences == 0:
    return 0
  else:
    return num_punct/num_sentences


def get_tweet_vector(tweet):
  weight_abolutist_metric = 4
  weight_pronouns_metric = 2
  weight_textblob = 1
  weight_anew_metric = 1
  weight_pos_metric = 1

  absolutist = [absolutist_words_metric(tweet)]*weight_abolutist_metric
  pronouns = [first_pronouns_metric(tweet)]*weight_pronouns_metric + [second_third_pronouns_metric(tweet)]*weight_pronouns_metric
  textblob = [TextBlob_metrics(tweet)[0]]*weight_textblob + [TextBlob_metrics(tweet)[1]]*weight_textblob
  anew = [anew_metric(tweet)[0]]*weight_anew_metric + [anew_metric(tweet)[1]]*weight_anew_metric + [anew_metric(tweet)[2]]*weight_anew_metric
  pos = [pronominalisation_index(tweet)]*weight_pos_metric + [readiness_to_action_index(tweet)]*weight_pos_metric + [punctuation_metric(tweet)]*weight_pos_metric

  tweet_vector = absolutist + pronouns + textblob + anew + pos
  
  return tweet_vector               


def get_tweet_data_vector(tweet_vector, timestamp, likes, retweets, sentimental):
  # timestamp = timestamp[:19]
  # timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

  time_vector =  [timestamp.month, timestamp.day, timestamp.hour, timestamp.minute]

  tweet_vector = ast.literal_eval(str(tweet_vector))
  metric = tweet_vector + time_vector + [likes, retweets] + [sentimental]*5
  return metric