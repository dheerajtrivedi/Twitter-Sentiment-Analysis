import tweepy

access_token = ''
access_token_secret = ''
consumer_key = ''
consumer_key_secret = ''
auth = tweepy.OAuthHandler( consumer_key, consumer_key_secret)
auth.set_access_token(access_token , access_token_secret)

api = tweepy.API(auth)

class PublicTweets:
    def __init__(self,query,c,res_type):
        self.public_tweets = []
        n = 0
        for tweet in tweepy.Cursor(api.search,
                           q= query,
                           count = c,
                           result_type=res_type,
                           include_entities=True).items():
                n = n+1
                if(n >= c): break
                self.public_tweets.append(tweet)
