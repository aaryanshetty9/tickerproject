import yfinance as yf
import praw
import config
import pandas as pd
from datetime import datetime, timedelta
from bullbearish import BullishBearish as b
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#VADER is specifically tuned to sentiments expressed in social media


#grabs ticker
tick = input("Enter a Ticker: ")

def download_vader_lexicon():
    nltk.download('vader_lexicon')


#initialize reddit api
reddit = praw.Reddit(
    client_id= config.client_id,
    client_secret= config.client_secret,
    user_agent= config.user_agent
)


#fetches 10 year financial data of any stock
def fetchdata(ticker):

    #fetch start and end date
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10*365)

    # Download the data
    data = yf.download(ticker, start=start_date, end=end_date)

    print(data)

    #returns data in pd data frame like: Date | Open | High | Low | Close | Adj Close | Volume
    return data
    


def gatherReddit(ticker):
    sid = SentimentIntensityAnalyzer()
    subreddit = reddit.subreddit('wallstreetbets')
    #min upvote + min comment, might remove to get more data
    #min_upvotes = 15
    #min_comments = 15
    tick_info = yf.Ticker(ticker)

    # Initialize a list to store dictionaries with post details
    posts_data = []
    keywords = [ticker, 'earnings', tick_info.info['shortName'], tick_info.info['industry']]
    title_sentiment_sum = 0

    # Fetch posts, max of 600 posts over the user
    for post in subreddit.search(ticker, time_filter='year', limit=600):
        # Check if post meets upvotes and comments criteria
        #if post.score >= min_upvotes and post.num_comments >= min_comments:
        if any(keyword.lower() in post.title.lower() for keyword in keywords):
            # Append a dictionary for each post to the list
            title_sentiment = sid.polarity_scores(post.title)
            title_sentiment_sum += title_sentiment['compound']
            posts_data.append({
                "Title": post.title,
                "Title Sentiment": title_sentiment['compound'],
                "Upvotes": post.score,
                "Comments": post.num_comments,
                #Convert the timestamp to a readable format
                "Date": datetime.fromtimestamp(post.created)
            })

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(posts_data)

    print(df)
    #returning df 
    return df

fetchdata(tick)
gatherReddit(tick)
#download_vader_lexicon()
