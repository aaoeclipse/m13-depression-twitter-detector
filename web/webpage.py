from email import utils
import streamlit as st
import pandas as pd
import pickle
import time

import utils as utils

from metrics import get_tweet_vector

# with open('lin.pkl', 'rb') as li:
#     lin_reg = pickle.load(li)


def main():
    def user_weights():
        st.sidebar.subheader("weights")
        weight_abolutist_metric = st.sidebar.slider(
            'weight_abolutist_metric', 1, 5, 4)
        weight_pronouns_metric = st.sidebar.slider(
            'weight_pronouns_metric', 0, 5, 2)
        weight_textblob = st.sidebar.slider('weight_textblob', 0.0, 1.0, .25)
        weight_anew_metric = st.sidebar.slider(
            'weight_anew_metric', 0.0, 1.0, .25)
        weight_pos_metric = st.sidebar.slider(
            'weight_pos_metric', 0.0, 1.0, .25)

        data = {
            'weight_abolutist_metric': weight_abolutist_metric,
            'weight_pronouns_metric': weight_pronouns_metric,
            'weight_textblob': weight_textblob,
            'weight_anew_metric': weight_anew_metric,
            'weight_pos_metric': weight_pos_metric,
        }
        features = pd.DataFrame(data, index=[0])
        return features

    def user_input():
        st.sidebar.subheader("Tweeter Data")
        absolutist = st.sidebar.slider('absolutist', 0.0, 10.0, 1.0)
        pronouns = st.sidebar.slider('pronouns', 0.0, 10.0, 1.0)
        textblob = st.sidebar.slider('textblob', 0.0, 10.0, 1.0)
        anew = st.sidebar.slider('anew', 0.0, 10.0, 1.0)
        pos = st.sidebar.slider('pos', 0.0, 10.0, 1.0)
        nlp_detect = st.sidebar.slider('depression_nlp', 0.0, 1.0, 0.5)

        data = {
            'absolutist': absolutist,
            'pronouns': pronouns,
            'textblob': textblob,
            'anew': anew,
            'pos': pos,
            "nlp_detect": nlp_detect
        }

        features = pd.DataFrame(data, index=[0])
        return features

    st.title('Twitter detection model')

    st.sidebar.subheader("Prediction Parameter")

    selection = st.sidebar.selectbox(
        "Predict by:", ["Twitter Acc", "Manual"])

    st.sidebar.subheader("Parameters")

    if selection == "Manual":
        user_weights()
        user_input()
    else:
        tweet = st.sidebar.text_input("tweeter account")

        if st.sidebar.button('fetch twitter account'):
            with st.spinner('Wait for it...'):
                parse_tweet = utils.get_twitter(tweet)
                try:
                    df = utils.fetch_tweets(parse_tweet)
                    st.write(df)
                except Exception:
                    st.write("Error on fetching tweet")
                
                
            st.success('Done!')
            st.write('Why hello there')
        else:
            st.write('Ready to fetch...')


    # sex_option = ['Male', 'Female']
    # sex = st.sidebar.selectbox("Sex", sex_option)
    # df = pd.DataFrame(get_tweet_vector(tweet), columns=[
    #                   list(str(x) for x in range(16))])
    # st.dataframe(df)
if __name__ == '__main__':
    main()
