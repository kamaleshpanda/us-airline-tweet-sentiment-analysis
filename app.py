import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment of Tweets About US Airlines")
st.sidebar.title("Sentiment of Tweets About US Airlines")
st.markdown("""
This interactive dashboard analyzes customer sentiment toward major U.S. airlines using Twitter data.  
Explore trends, service issues, and overall public perception through dynamic visualizations.
""")
st.sidebar.markdown("Use filters to explore airline sentiment insights.")
Data_Path = r"C:\Users\KIIT0001\PycharmProjects\us-airline-tweet-sentiment-analysis\Tweets_cleaned.csv"

@st.cache_data(persist=True)
def loaddata():
    dataframe = pd.read_csv(Data_Path)
    dataframe['tweet_created'] = pd.to_datetime(dataframe['tweet_created'])
    return dataframe
data = loaddata()
## st.write(data) ## ??to show all the data .... used only for debugging purpose
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

st.sidebar.subheader("Breakdown Airline Tweets by Sentiment")
choice = st.sidebar.multiselect("Pick Airlines",('US Airways','United','SouthWest','Delta','American'),key=4)

if len(choice)>0:
    choice_data = data[data['airline'].isin(choice)]
    fig_choice = px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count',color='airline_sentiment'
                              ,facet_col='airline_sentiment',labels={'airline_sentiment':'tweets'},height=600,width=800)
    st.plotly_chart(fig_choice)

##Facets = splitting one big chart into multiple small charts based on a category.
## So Plotly created separate mini charts for:Positive,Negative and Neutral tweets

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment',('positive','negative','neutral'))

if not st.sidebar.checkbox("Hide",True,key=6):
    st.header('Word cloud for %s sentiment'%word_sentiment)
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split()if 'http' not in word
                                and not word.startswith('@')])
##@Delta I am VERY disappointed 😡😡!! Flight delayed again... check http://t.co/abc #worst
##this gets cleaned to "I am VERY disappointed 😡😡!! Flight delayed again... check #worst"
    # Create word cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        stopwords=STOPWORDS
    ).generate(processed_words)
    #plt.imshow(wordcloud)
    #plt.xticks([]) ##removes numbers/ticks from X axis
    #plt.yticks([]) ####removes numbers/ticks from Y axis
    #st.pyplot() # old way (top 3 lines )
    fig, ax = plt.subplots(figsize=(10,5)) #width 10 height 5 inch
    ax.imshow(wordcloud, interpolation='bilinear') #displays image and smooths the image
    ax.set_axis_off() #removes ticks from both axis
    st.pyplot(fig)
