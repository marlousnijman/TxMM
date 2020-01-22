import re
import pandas as pd
import matplotlib.pyplot as plt
from pattern.text.nl import sentiment
from collections import Counter
import demoji

# demoji.download_codes()

# https://eikhart.com/blog/dutch-stopwords-list
with open('stopwords.txt', 'r') as f:
    stop_words = f.read().splitlines()

pd.set_option('max_colwidth', 200)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)

tweets = pd.read_csv("tweets.csv", encoding='utf-8')
print(tweets['political_party'].value_counts())  # Count tweets per party


# Clean the tweet text
# Stop words are not removed, because words like 'niet' are important for sentiment analysis
def clean_tweets(tweet):
    tweet = tweet.lower() # String to lower case
    tweet = re.sub("@[A-Za-z0-9]+","", tweet) # Remove mentions
    tweet = re.sub("http\S+", "", tweet) # Remove links
    tweet = re.sub(r'[^\w\s]', '', tweet) # Remove punctuation
    tweet = demoji.replace(tweet, "")
    tweet = tweet.replace("\n", " ") # Remove new lines

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


# Compute the polarity and subjectivity for every tweet
def compute_sentiment(tweets):
    tweets["polarity"] = tweets["processed_tweets"].apply(lambda x: sentiment(x)[0])
    tweets["subjectivity"] = tweets["processed_tweets"].apply(lambda x: sentiment(x)[1])
    return tweets


# Plot the average sentiment for each party
def plot_sentiment(tweets):
    average_polarity = tweets.groupby('political_party')['polarity'].mean().sort_values(ascending=False)
    average_polarity.plot.bar(color="pink")
    plt.xlabel("Political Party")
    plt.ylabel("Average Polarity")
    plt.title("Sentiment of Dutch Political Parties on Twitter")
    plt.tight_layout()
    plt.savefig("plots/sentiment.png")
    plt.show()


# Tokenizes tweets
def tokenize(tweet):
    return tweet.split()


# Compute topics that political parties tweet about
def compute_topics(tweets):
    topic_tweets = tweets[['political_party', 'processed_tweets']]
    topic_tweets['processed_tweets'] = topic_tweets['processed_tweets'].apply(remove_stopwords) # Remove stopwords
    topic_tweets['processed_tweets'] = topic_tweets.groupby('political_party')['processed_tweets'].transform(lambda x: ' '.join(x))
    topic_tweets = topic_tweets[['political_party', 'processed_tweets']].drop_duplicates().reset_index(drop=True)
    topic_tweets["bag_of_words"] = topic_tweets['processed_tweets'].apply(tokenize)
    topic_tweets['word_frequencies'] = topic_tweets['bag_of_words'].apply(Counter)
    topic_tweets['topics'] = topic_tweets['word_frequencies'].apply(lambda x: x.most_common(15))
    topic_tweets['topics'] = topic_tweets['topics'].apply(lambda x: dict(x).keys())

    print(topic_tweets[['political_party', 'topics']])


tweets = clean_data(tweets)
tweets = compute_sentiment(tweets)
compute_topics(tweets)
plot_sentiment(tweets)