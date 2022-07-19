import pandas as pd

home_path="."
df = pd.read_csv(f"{home_path}/users_timelines.csv")


df = df[df['language'] == 'en'] # only keep tweets in english
df = df[df['urls'] == '[]'] #Remove tweets with links
df = df[df['photos'] == '[]'] #Remove tweets with photos
df = df[df['video'] == 0] #Remove tweets with videos
# df = df[df['reply_to'] == '[]'] # remove replies


# Remove the columns that are not needed
df.drop(columns=['id', 'conversation_id', 'date', 'time', 'timezone',
       'user_id', 'name', 'place', 'mentions', 'retweet',
       'replies_count','hashtags', 'cashtags', 'link', 'quote_url', 
       'thumbnail', 'near', 'geo', 'source', 'user_rt_id', 'user_rt',
       'retweet_id', 'reply_to', 'retweet_date', 'translate', 'trans_src',
       'trans_dest','urls', 'photos', 'video'], inplace=True)

# Use Groupby to only keep user that have more than 20 tweets
dfg =df.groupby('username')
cond_users = dfg['username'].count() >= 20
valid_users = cond_users[cond_users].index.to_list()
df = df[df['username'].isin(valid_users)]


# Remove any extra tweets and only keep the latest 20 tweets per user.
df = df.sort_values(by=['username', 'created_at'], ascending=False)
df.reset_index(inplace=True)
df_iter = df.copy()

prev_user = ""
count = -1
for ind, row in df_iter.iterrows():
    curr_user = row['username']
    if curr_user != prev_user:
        count = 1
    else:
        count += 1
    if count > 20:
        df = df.drop(ind)
    prev_user = curr_user


# Rename the colu,ns and save the df 
df = df.rename(columns={"created_at":"timestamp", "username":"userID", "language":"lang",
            "retweets_count":"retweet_count", "likes_count":"favorite_count"})
df = df.drop(columns=['index'])
df.to_csv(f'{home_path}/cleaned_depressed_tweets_replies.csv', index=False)