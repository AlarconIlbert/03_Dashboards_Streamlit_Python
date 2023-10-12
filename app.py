import streamlit as st
import pandas as pd
import numpy as np

st.title('Sentimental Analysis of Tweets about US Airlines! 🐦')
st.sidebar.title('Sentimental Analysis of Tweets about US Airlines!')

st.markdown("This application is a Street dashboard to analyze the sentimental of Tweets 🐦")
st.sidebar.markdown("This application is a Street dashboard to analyze the sentimental of Tweets 🐦")

@st.cache_data
def load_data (nrows):
    data_df = pd.read_csv("data\Tweets.csv", nrows=nrows,)
    data_df['tweet_created'] = pd.to_datetime(data_df['tweet_created'])
    return data_df

tweet_df=load_data(100000)

st.sidebar.subheader("Show raw Tweet")
random_tweet = st.sidebar.radio("Sentiment", ('positive', 'neutral', 'negative'))
st.sidebar.markdown(tweet_df.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.