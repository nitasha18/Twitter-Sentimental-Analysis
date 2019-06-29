import re
import tweepy
import nltk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from datetime import datetime, timedelta
from nltk.tokenize import WordPunctTokenizer
from tkinter import Tk, Label, INSERT, END, Entry, Button, Toplevel

ACC_TOKEN=''
ACC_SECRET=''
CONS_KEY=''
CONS_SECRET=''

pos = 0  # total positive tweets count
neg = 0  # total negative tweets count
neut = 0  # total neutral tweets count
final_score=0

#connects to Twitter API
def authentication(acc_token,acc_secret,cons_key,cons_secret):
    auth=tweepy.OAuthHandler(cons_key,cons_secret)
    auth.set_access_token(acc_token,acc_secret)
    API=tweepy.API(auth)
    return API

#searching the Tweepts
def search_tweets(keyword,total_tweets):
    today_datetime=datetime.today().now()
    yesterday_datetime=today_datetime-timedelta(days=1)
    today_date=today_datetime.strftime('%Y-%m-%d')                  #getting today's date
    yesterday_date=yesterday_datetime.strftime('%Y-%m-%d')          #getting yesterday's date
    API=authentication(ACC_TOKEN,ACC_SECRET,CONS_KEY,CONS_SECRET)   #connecting to Twitter
    search_result=tweepy.Cursor(API.search,                         #twitter search
                                q=keyword,                          #keyword which needs to be searched
                                since=yesterday_date,               #defining time period over which the result will be given
                                result_type='recent',               #going to take newest tweets
                                lang='en'                           #english tweets only
                                ).items(total_tweets)               #maximum tweets going to take
    return search_result

#cleaning the tweets
def clean_tweet(tweet):
    username_removed=re.sub(r'@[A-Za-z0-9]+','',tweet.decode('utf-8')) #removing the username from every tweets
    #print(username_removed)
    links_removed=re.sub('https?://[A-Za-z0-9./]+','',username_removed) #links removed from the tweets
    #print(links_removed)
    number_removed=re.sub('[^a-zA-Z]', ' ',links_removed)                  #removing numbers too
    #print(numer_removed)
    lower_case=number_removed.lower()                                   #to convert eh string into lowercase
    #print(lower_case)
    w=WordPunctTokenizer()                                              #to remove the unecessary spaces
    words_list=w.tokenize(lower_case)
    final_tweet=' '.join(words_list)
    return final_tweet

#finding the sentiment score
def get_sentiment_score(tweet):
    SA=TextBlob(tweet)
    global pos
    global neg
    global neut
    if(SA.sentiment[0]>0.0):
        pos+=1
    elif SA.sentiment[0]<0.0:
        neg+=1
    elif SA.sentiment[0]==0:
        neut+=1
    return SA.sentiment[0]

#analyzing tweets
def analyze_tweets(keyword,total_tweets):
    f_score=0
    global final_score
    tweets=search_tweets(keyword,total_tweets)
    for tweet in tweets:
        c_tweet=clean_tweet(tweet.text.encode('utf-8'))
        score=get_sentiment_score(c_tweet)
        f_score+=score
        if score>0.0:
            status= str(score)+' || POSITIVE'
        elif score<0.0:
            status= str(score)+' || NEGATIVE'
        elif score==0.0:
            status= str(score)+' || NEUTRAL'
        print('Tweet: {}'.format(c_tweet))
        print('Overall analysis: {}'.format(status))
    final_score=round((f_score/float(total_tweets)),2)
    return final_score

def display_result(final_score):
    global final_status
    if max(pos,neg,neut)==pos:
        f_status=' || POSITIVE ||'
    elif max(pos,neg,neut)==neg:
        f_status=' || NEGATIVE ||'
    elif max(pos,neg,neut)==neut:
        f_status=' || NEUTRAL ||'
    final_status = str(final_score) + f_status
    return final_status

def draw_graphs(labels, sizes):
    g1=plt.figure(1)                #draw pie chart chart
    colors = ['gold', 'yellowgreen', 'lightskyblue']
    plt.pie(sizes,labels=labels,colors=colors,autopct='%1.1f%%')
    plt.title('Tweets')
    plt.axis('equal')
    g2=plt.figure(2)                #draw bar graph
    y_pos = np.arange(len(labels))
    plt.bar(y_pos, sizes, align='center', alpha=0.5)
    plt.xticks(y_pos, labels)
    plt.ylabel('Total Counts')
    plt.xlabel('Response')
    plt.title('Tweets')
    plt.show()

def GUI_graph():
    labels=['Positive','Negative','Neutral']
    sizes=[pos,neg,neut]
    draw_graphs(labels,sizes)      #draw pie and bar graph

#GUI for displaying main result
def GUI_displaying_score():
    root1=Tk()
    welcome=Label(root1,text='\n')
    welcome.pack()
    text0=Label(root1,
               text='Twitter Sentimental Analysis on \''+keyword+'\'',
               font='Times 28')
    text1=Label(root1,
               text='Positive tweets: '+str(pos)+'\nNegative tweets: '+str(neg)+'\nNeutral tweets: '+str(neut)+'\nFinal score: '+str(final_score),
               font='Times 21')

    text0.pack()
    text1.pack()
    welcome0 = Label(root1, text='\n')
    welcome0.pack()
    root.mainloop()

def display_curr(root,keyword,limit):
    dis0_text=Label(root,text='Keyword Searched: \''+keyword+'\' , Tweets Limit: '+str(limit)+'\n',font='Times 24')
    dis0_text.pack()
    score_analysis = Button(root, text='Score Analysis', font=inp_font, command=GUI_displaying_score)
    score_analysis.pack()
    space1 = Label(root, text='\n')
    space1.pack()
    graph= Button(root,text='Graph Analysis',font=inp_font,command=GUI_graph)
    graph.pack()
    space2 = Label(root, text='\n')
    space2.pack()
    exit_button = Button(root, text='Exit Window',font=inp_font, command=root.destroy)
    exit_button.pack()
    root.mainloop()

#GUI
root=Tk()
root.geometry("1000x700+210+130")
inp_font=('Times',21)
inp_text1=Label(root,text='Enter the keyword for analysis: ',font='Times 24').pack()
entry1= Entry(root,font=inp_font)
entry1.pack()
entry1.insert(INSERT,'')

inp_text2=Label(root,text='Enter the Tweets\'s Limit: ',font='Times 24').pack()
entry2= Entry(root,font=inp_font)
entry2.pack()
entry2.insert(INSERT,' ')

def print_content():
    global keyword
    global limit
    global final_score
    keyword=str(entry1.get()).strip()
    limit=int(entry2.get())
    entry1.delete(0,END)
    entry2.delete(0,END)
    final_score = display_result(analyze_tweets(keyword, limit))
    space=Label(root,text='\n')
    space.pack()
    display_curr(root,keyword,limit)
    print('-----------------------------------------')
    print('->Positive: ' + str(pos))
    print('->Negative: ' + str(neg))
    print('->Neutral: ' + str(neut))
    print('-----------------------------------------')
    print('->Final score: ' + final_score)
    print('-----------------------------------------')

button=Button(root,text='Submit',font=inp_font,command=print_content)
button.pack()
root.mainloop()








