import re
import tweepy
import nltk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from datetime import datetime, timedelta
from ntlk.tokenize import WordPunctTokenizer

ACC_TOKEN=''
ACC_SECRET=''
CONS_KEY=''
CONS_SECRET=''
pos=0   #total positive tweets count
neg=0   #total negative tweets count
neut=0  #total neutral tweets count

#connects to Twitter API
def authentication(acc_token,acc_secret,cons_key,cons_secret):
    auth=tweepy.OAuthHandler(cons_key,cons_secret)
    auth.set_access_token(acc_token,acc_secret)
    API=tweepy.API(auth)
    return API

#searching the Tweepts
def search_tweets(keyword,total_tweets):
    today_datetime=datetime.today().now()
    yesterday_datetime=today_datetime-timedelta(day=1)
    today_date=today_datetime.strftime('%Y-%m-%d')  #getting today's date
    yesterday_date=yesterday_datetime.strftime('%Y-%m-%d')  #getting yesterday's date
    API=authentication(ACC_TOKEN,ACC_SECRET,CONS_KEY<CONS_SECRET)   #connecting to Twitter
    search_result=tweepy.Cursor(API.search,             #twitter search
                                q=keyword,              #keyword which needs to be searched
                                since=yesterday_date,   #defining time period over which the result will be given
                                result_type='recent',   #going to take newest tweets
                                lang='en'               #english tweets only
                                ).items(total_tweets)   #maximum tweets going to take
    return search_result

#cleaning the tweets
def clean_tweet(tweet):
    username_removed=re.sub(r'@[A-Z]a-z0-9]+','',tweet.decode('utf-8')) #removing the username from every tweets
    #print(username_removed)
    links_removed=re.sub('https?://[A-Za-z0-9./]+','',username_removed) #links removed from the tweets
    #print(links_removed)
    number_removed=re.sub('[a-zA-Z]','',links_removed)  #removing numbers too
    #print(numer_removed)
    lower_case=number_removed.lower()   #to convert eh string into lowercase
    #print(lower_case)
    #to remove the unecessary spaces
    w=WordPunchTokenizer()
    words_list=w.tokenize(lower_case_tweet)
    final_tweet=(' '.join(words_list)).strip()
    return final_tweet

#finding the sentiment score
def get_sentiment_score(tweet):
    SA=textBlob(tweet.text)
    if(SA.sentiment[0]>0.0):
        pos+=1
    elif SA.sentiment[0]<0.0:
        neg+=1
    elif SA.sentiment[0]==0:
        neut+=1
    #finding which has max score
    if(max(pos,neg,neut)==pos):
        return pos+' POSITIVE | ✅'
    elif(max(pos,neg,neut)==neg):
        return neg+' NEGATIVE | ❌'
    elif(max(pos,neg,neut)==neut):
        return neut+' NEUTRAL | 🔶'


#analysing tweets
def analyze_tweets(keyword,total_tweets):
    score=0
    tweets=search_tweets(keyword,total_tweets)
    for tweet in tweets:
        c_tweet=clean_tweet(tweet.text.encode('utf-8'))
        score=get_sentiment_score(c_tweet)
        print('Tweet: {}'.format(c_tweet))
        print('Score: {}'.format(score))
    final_score=round((score/float(total_tweets)),2)
    return final_score

keyword='AUSVSENG'
final_score=analyze_tweets(keyword,100)