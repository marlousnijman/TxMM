from tweepy import OAuthHandler, API
import unicodecsv

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

political_parties = ["VVD",
                     "PvdA",
                     "geertwilderspvv",
                     "fvdemocratie",
                     "cdavandaag",
                     "groenlinks",
                     "D66",
                     "SPnl",
                     "50pluspartij",
                     "christenunie"]

with open('tweets.csv', mode= 'wb') as tweets_file:
    tweet_writer = unicodecsv.writer(tweets_file, delimiter=',')
    tweet_writer.writerow(["political_party",
                           "tweet_text",
                           "reply"])
    for political_party in political_parties:
        tweets = api.user_timeline(screen_name=political_party, count=10, tweet_mode='extended')
        for tweet in tweets:
            reply = tweet.in_reply_to_status_id != ""
            tweet_writer.writerow([political_party,
                                   tweet.full_text,
                                   reply])