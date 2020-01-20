import re
import nltk
import string
import pandas as pd
from nltk.corpus import stopwords

# nltk.download('stopwords')

stop_words = set(stopwords.words('dutch'))

pd.set_option('max_colwidth', 200)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)

tweets = pd.read_csv("tweets.csv")
print(tweets['political_party'].value_counts())  # Count tweets per party


# Clean the tweet text
def clean_tweets(tweet):
    tweet = tweet.lower() # String to lower case
    tweet = re.sub("@[A-Za-z0-9]+","", tweet) # Remove mentions
    tweet = re.sub("http\S+", "", tweet) # Remove links
    tweet = tweet.translate(None, string.punctuation) # Remove punctuation
    tweet = tweet.replace("\n", " ")
    tweet = remove_stopwords(tweet)

    return tweet

# Remove stopwords from a tweet
def remove_stopwords(tweet):
    tweet_tokens = tweet.split()
    tweet_tokens = [w for w in tweet_tokens if not w in stop_words]
    tweet = ' '.join(word for word in tweet_tokens)

    return tweet


# Clean the data
def clean_data(tweets):
    tweets = tweets[tweets['retweet'] == False] # Remove retweets
    tweets = tweets[tweets['reply'] == False] # Remove replies
    tweets["processed_tweets"] = tweets['tweet_text'].apply(clean_tweets)

    return tweets


tweets = clean_data(tweets)
print(tweets['processed_tweets'])
print(tweets['political_party'].value_counts())  # Count tweets per party