import pandas as pd
from pattern.text.nl import sentiment

tweets = pd.read_csv("tweets.csv")
print(tweets.head())