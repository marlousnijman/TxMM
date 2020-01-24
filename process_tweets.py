### Imports

import re
import os
import pandas as pd
import matplotlib.pyplot as plt
from pattern.text.nl import sentiment
from collections import Counter
import demoji
from wordcloud import WordCloud


### Downloads

# demoji.download_codes()


### Settings

pd.set_option('max_colwidth', 200)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
pd.options.mode.chained_assignment = None  # Turn off warnings


### Functions

# Show information about tweet data set
def show_data_summary(tweets_df):
    print(tweets_df['political_party'].value_counts())  # Count tweets per party


# Load stop words
def load_textfile(file_name):
    with open(file_name, 'r') as f:
        file_content = f.read().splitlines()

    return file_content


# Clean the tweet text (stop words are not removed, because words like 'niet' are important for sentiment analysis)
def clean_tweets(tweet):
    tweet = tweet.lower()  # String to lower case
    tweet = re.sub("@[A-Za-z0-9]+", "", tweet)  # Remove mentions
    tweet = re.sub("http\S+", "", tweet)  # Remove links
    tweet = re.sub(r'[^\w\s]', "", tweet)  # Remove punctuation
    tweet = demoji.replace(tweet, "") # Remove emojis
    tweet = tweet.replace("\n", " ")  # Remove new lines

    return tweet


# Tokenizes tweets
def tokenize(tweet):
    return tweet.split()


# Remove stopwords from a tweet
def remove_stopwords(tweet, stop_words):
    tweet_tokens = tokenize(tweet)
    tweet_tokens = [w for w in tweet_tokens if not w in stop_words]
    tweet = ' '.join(word for word in tweet_tokens)

    return tweet


# Clean the data
def clean_data(tweets_df):
    tweets_df = tweets_df[tweets_df['retweet'] == False]  # Remove retweets
    tweets_df = tweets_df[tweets_df['reply'] == False]  # Remove replies
    tweets_df["clean_tweets"] = tweets_df['tweet_text'].apply(clean_tweets)

    return tweets_df


# Compute the polarity and subjectivity for every tweet
def compute_sentiment(tweets_df):
    tweets_df["polarity"] = tweets_df["clean_tweets"].apply(lambda x: sentiment(x)[0])
    tweets_df["subjectivity"] = tweets_df["clean_tweets"].apply(lambda x: sentiment(x)[1])

    return tweets_df


# Plot the average sentiment for each party
def plot_sentiment(tweets_df):
    average_polarity = tweets_df.groupby('political_party')['polarity'].mean().sort_values(ascending=False)
    average_polarity.plot.bar(color="pink")
    plt.xlabel("Political Party")
    plt.ylabel("Average Polarity")
    plt.title("Sentiment of Dutch Political Parties on Twitter")
    plt.tight_layout()
    plt.savefig("plots/sentiment.png")
    plt.close()


# Compute topics that political parties tweet about
def compute_topics(tweets_df):
    tweets_df = tweets_df[['political_party', 'clean_tweets']]
    stop_words = load_textfile('stopwords.txt')  # https://eikhart.com/blog/dutch-stopwords-list
    tweets_df['clean_tweets'] = tweets_df['clean_tweets'].apply(lambda x: remove_stopwords(x, stop_words))
    tweets_df['clean_tweets'] = tweets_df.groupby('political_party')['clean_tweets'].transform(lambda x: ' '.join(x))
    tweets_df = tweets_df[['political_party', 'clean_tweets']].drop_duplicates().reset_index(drop=True)
    tweets_df["bag_of_words"] = tweets_df['clean_tweets'].apply(tokenize)
    tweets_df['word_frequencies'] = tweets_df['bag_of_words'].apply(Counter)
    tweets_df['topics'] = tweets_df['word_frequencies'].apply(lambda x: x.most_common(50))
    tweets_df['topics'] = tweets_df['topics'].apply(lambda x: dict(x))

    return tweets_df[['political_party', 'topics']]


# Generate a word cloud for a string of wowrds
def generate_word_cloud(words, party):
    word_cloud = WordCloud(background_color="white", colormap='RdPu').generate_from_frequencies(words)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("plots/topics_"+party+".png")
    plt.close()


# Create word clouds from the lists of topics discussed for each party
def topics_to_word_cloud(topic_tweets):
    topic_tweets.apply(lambda x: generate_word_cloud(x.topics, x.political_party),  axis=1)


# Assign a tweet a label if it contains a word from the topic list
def assign_label(tweet, topic_list):
    if [w for w in topic_list if w in tweet]:
        return True
    else:
        return False


# For all topics, assign a label to a tweet if it is about that topic
def compute_labels(tweets_df):
    for filename in os.listdir('topics'):
        topic = filename.replace('.txt', '')
        topic_words = load_textfile('topics/'+filename)
        tweets_df[topic] = tweets_df['clean_tweets'].apply(lambda x: assign_label(x, topic_words))

    return tweets_df


# Compute sentiments and topics and plot them
def main():
    tweets = pd.read_csv("tweets.csv", encoding='utf-8')
    tweets = clean_data(tweets)
    show_data_summary(tweets)
    tweets = compute_sentiment(tweets)
    topics = compute_topics(tweets)
    plot_sentiment(tweets)
    topics_to_word_cloud(topics)
    tweets = compute_labels(tweets)


# Run main
if __name__ == '__main__':
    main()