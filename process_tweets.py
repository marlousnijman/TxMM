import pandas as pd
from pattern.text.nl import sentiment

pd.set_option('max_colwidth', 10)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)

tweets = pd.read_csv("tweets.csv")

tweets["polarity"] = tweets["tweet_text"].apply(lambda x: sentiment(x)[0])
tweets["subjectivity"] = tweets["tweet_text"].apply(lambda x: sentiment(x)[1])
print(tweets)