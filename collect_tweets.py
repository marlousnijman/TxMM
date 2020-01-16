from tweepy import OAuthHandler, API
import unicodecsv
import datetime

consumer_key="hxyzr33lfxrot5D8TnjdLvY4q"
consumer_secret="ObHwYFXPtPLKzMUuHj7D5tnmqSliYfsiAuFzr1R4fRTrrVlt8P"
access_token="239026422-RhrqJe0kHS3PouRW0904XXYS2LYFZTnCj9jMQp7b"
access_token_secret="lef6BN8K0q4MMjQq9fKb2KgnjWmnpncu9Tv99nZPp0CX6"

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

startDate = datetime.datetime(2019, 1, 1, 0, 0, 0)
endDate = datetime.datetime(2020, 1, 1, 0, 0, 0)

with open('tweets.csv', mode= 'wb') as tweets_file:
    tweet_writer = unicodecsv.writer(tweets_file, delimiter=',')
    tweet_writer.writerow(["political_party",
                           "tweet_text",
                           "date",
                           "reply",
                           "retweet"])
    for political_party in political_parties:
        tweets = api.user_timeline(screen_name=political_party, tweet_mode='extended')
        for tweet in tweets:
            reply = tweet.in_reply_to_status_id is not None
            retweet = tweet.full_text.startswith("RT @")
            correct_date = endDate > tweet.created_at > startDate
            if correct_date:
                tweet_writer.writerow([political_party,
                                       tweet.full_text,
                                       tweet.created_at,
                                       reply,
                                       retweet])