import scraper as s
import Tkinter
import ttk
import tkMessageBox
import pandas as pd
import matplotlib.pyplot as plt
import pylab
import webbrowser
import re
from textblob import TextBlob

def graph():
    query = t1.get()
    c = int(t2.get())
    graph_type = cb.get()
    if(graph_type == ''):
        tkMessageBox.showinfo('Error', 'Choose a graph type!')
        return

    pt = s.PublicTweets(query,c,'mixed')

    tweets = pd.DataFrame()

    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel(graph_type, fontsize=15)
    ax.set_ylabel('Number of tweets' , fontsize=15)
    ax.set_title('Top 5 ' + graph_type, fontsize=15, fontweight='bold')

    if(graph_type == 'Language'):
        tweets['lang'] = map(lambda status: status.lang, pt.public_tweets)
        tweets_by_lang = tweets['lang'].value_counts()
        tweets_by_lang[:5].plot(ax=ax, kind='bar', color='blue')
    elif(graph_type == 'Hashtags'):
        hashtags = []
        for tweet in pt.public_tweets:
            for hashtag in tweet.entities['hashtags']:
                hashtags.append(hashtag['text'])
        tweets['hashtag'] = map(lambda hashtag: hashtag, hashtags)
        tweets_by_hashtag = tweets['hashtag'].value_counts()
        tweets_by_hashtag[:5].plot(ax=ax, kind='bar', color='green')
    elif(graph_type == 'User mentions'):
        mentions = []
        for tweet in pt.public_tweets:
            for user_mention in tweet.entities['user_mentions']:
                mentions.append(user_mention['screen_name'])
        tweets['mention'] = map(lambda mention: mention, mentions)
        tweets_by_mentions = tweets['mention'].value_counts()
        tweets_by_mentions[:5].plot(ax=ax, kind='bar', color='green')

    pylab.show()

def retweeted():
    query = t1.get()
    c = int(t2.get())
    pt = s.PublicTweets(query,c,'popular')
    pt.public_tweets.sort(key = lambda tweet: tweet.retweet_count)
    most_retweet = pt.public_tweets[-1]
    tweet_url = 'http://twitter.com/'+most_retweet.user.screen_name+'/status/'+most_retweet.id_str
    webbrowser.open_new(tweet_url)

def favourite():
    query = t1.get()
    c = int(t2.get())
    pt = s.PublicTweets(query,c,'popular')
    for st in pt.public_tweets:
        print st.favorite_count
    pt.public_tweets.sort(key = lambda tweet: tweet.favorite_count)
    most_favorite = pt.public_tweets[-1]
    tweet_url = 'http://twitter.com/'+most_favorite.user.screen_name+'/status/'+most_favorite.id_str
    webbrowser.open_new(tweet_url)

def sentiment():
    query = t1.get()
    c = int(t2.get())
    pt = s.PublicTweets(query,c,'popular')
    pt.public_tweets.sort(key = lambda tweet:pol(tweet.text))
    print "Positive Tweets: "
    print pt.public_tweets[1].text
    print pt.public_tweets[2].text
    print pt.public_tweets[3].text
    print pt.public_tweets[4].text
    print pt.public_tweets[5].text

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def pol(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    return analysis.sentiment.polarity

top = Tkinter.Tk()
l1 = Tkinter.Label(top, text = 'Enter Query: ')
t1 = Tkinter.Entry(top, bd = 5)
l2 = Tkinter.Label(top, text = 'Enter Tweet Count: ')
t2 = Tkinter.Entry(top, bd = 5)
l1.pack()
t1.pack()
l2.pack()
t2.pack()

cb = ttk.Combobox(state = 'readonly', values = ['Language', 'Hashtags', 'User mentions'])
cb.pack()
b1 = Tkinter.Button(text = 'Show Graph', command = graph)
b1.pack()
b2 = Tkinter.Button(text = 'Sentiment Analysis',command = sentiment)
b2.pack()

top.mainloop()
