from email import utils
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

import utils as utils


# with open('lin.pkl', 'rb') as li:
#     lin_reg = pickle.load(li)


def main():
    image = Image.open('web/img/Group_52.png')

    
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

    st.image(image)


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
                try:
                    prob_of_depression = utils.full_process(tweet)[0][1]

                    labels = 'Depressed', 'Normal'
                    sizes = [(prob_of_depression*100), 100-(prob_of_depression*100)]
                    explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
                    fig1, ax1 = plt.subplots()
                    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                            shadow=True, startangle=90)
                    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                    st.pyplot(fig1)
                    st.write(f"Probability of being depressed: {prob_of_depression*100:.2f}%")
                    
                except Exception as e:
                    st.error("Error on fetching tweet: {}".format(e))
        else:
            st.write('Ready to fetch...')


    # sex_option = ['Male', 'Female']
    # sex = st.sidebar.selectbox("Sex", sex_option)
    # df = pd.DataFrame(get_tweet_vector(tweet), columns=[
    #                   list(str(x) for x in range(16))])
    # st.dataframe(df)
if __name__ == '__main__':
    main()
