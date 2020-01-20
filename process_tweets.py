import re
import nltk
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from pattern.text.nl import sentiment

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
    tweet = tweet.replace("\n", " ") # Remove new lines
    tweet = remove_stopwords(tweet) # Remove stopwords

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


def compute_sentiment(tweets):
    tweets["polarity"] = tweets["tweet_text"].apply(lambda x: sentiment(x)[0])
    tweets["subjectivity"] = tweets["tweet_text"].apply(lambda x: sentiment(x)[1])
    return tweets


tweets = clean_data(tweets)
tweets = compute_sentiment(tweets)

average_polarity = tweets.groupby('political_party')['polarity'].mean().sort_values(ascending=False)
average_polarity.plot.bar(color="pink")
plt.xlabel("Political Party")
plt.ylabel("Average Polarity")
plt.title("Sentiment of Dutch Political Parties on Twitter")
plt.tight_layout()
plt.savefig("plots/sentiment.png")
plt.show()