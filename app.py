import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


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

st.sidebar.markdown('## Number of Twqeet by sentiment')
select = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie Chart'], key=1)
sentiment_count = tweet_df['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})


if not st.sidebar.checkbox('Hide', True):
    st.markdown('## Number of Twqeet by sentiment')
    if select == 'Histogram':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)

    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader('When and where are users Tweeting from?')
hour = st.sidebar.slider('Hour of today', 0, 23)
modified_data = tweet_df[tweet_df['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Close", True, key=2):
    st.markdown('## Tweets location based on the time of day')
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data",False):
        st.write(tweet_df)
    
st.sidebar.subheader("Breakdown airline Tweet by sentiment")
choice = st.sidebar.multiselect('Pick airlines', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key=3)

if len(choice) > 0:
    choice_data = tweet_df[tweet_df.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment',
                              facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive','neutral', 'negative'))

if not st.sidebar.checkbox('Close', True, key=4):
    st.subheader('Word cloud for %s sentiment' % (word_sentiment))
    df = tweet_df[tweet_df['airline_sentiment'] == word_sentiment]
    words = ''.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()