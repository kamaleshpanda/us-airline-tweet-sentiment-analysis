import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Sentiment of Tweets About US Airlines")
st.sidebar.title("Sentiment of Tweets About US Airlines")
st.markdown("This is a streamlit dashboard to analyze sentiments of tweets 🛬🛩️")
st.sidebar.markdown("This is a streamlit dashboard to analyze sentiments of tweets 🛬🛩️")

Data_Path = r"C:\Users\KIIT0001\PycharmProjects\us-airline-tweet-sentiment-analysis\Tweets_cleaned.csv"

@st.cache_data(persist=True)
def loaddata():
    dataframe = pd.read_csv(Data_Path)
    dataframe['tweet_created'] = pd.to_datetime(dataframe['tweet_created'])
    return dataframe
data = loaddata()
## st.write(data) ## ??to show all the data .... used only for debugging puprose
st.sidebar.subheader("Show Random tweets")
random_tweet = st.sidebar.radio("Sentiment",('positive','negative','neutral'))
## st.sidebar.markdown(data.query("airline_sentiment == @random_tweet").sample(n=2)["text"].iat[0])
## making it easy
sampled = (data.query("airline_sentiment == @random_tweet").sample(n=1)["text"])
st.sidebar.markdown(sampled.iat[0])

st.sidebar.markdown("## Number of Tweets by Sentiment")
select = st.sidebar.selectbox('Visualization Type',['Histogram','Bar Chart'],key = '1')
sentiment_count = data['airline_sentiment'].value_counts()
## st.write(sentiment_count) ##to have a check
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index,'Tweets':sentiment_count.values})

if not st.sidebar.checkbox("Hide",True):
    st.markdown("## Number of Tweets by Sentiment")
    if select == 'Histogram':
        fig = px.bar(sentiment_count,x='Sentiment',y='Tweets',color='Sentiment')
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count,values='Tweets',names='Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader('When and Where are users tweeting From ?')
hour = st.sidebar.slider('Hour', 1, 24)
modified_data = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Hide", True, key=2):
    st.markdown("#### Tweets location map (simulated)")
    st.map(modified_data[['lat', 'lon']])
    st.caption("Locations are simulated for visualization purposes")

if st.sidebar.checkbox("Show Raw Data", False, key=3):
    st.write(modified_data)



