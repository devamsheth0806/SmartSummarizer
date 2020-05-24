from __future__ import  print_function
import os
import tweepy as tw
import re
import pandas as pd
import numpy as np 
import nltk
import math
import mglearn
import pyLDAvis
import pyLDAvis.sklearn
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.corpus import stopwords
import facebook
from os import path
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS
import feedparser
LANGUAGE = "english"

def social_driver():
	#print(posts['data'])
	print("#######################################################################################################################")
	print("################################  Data extraction and summarization from Social Media  ################################")
	print("#######################################################################################################################\n")

	while True:
	    p=0
	    print("\n                        Main Menu                      ")
	    print("_________________________________________________________")
	    print("1. Extract data from facebook posts and twitter tweets.")
	    print("2. Extract data from RSS Feeds.")
	    print("3. Exit.\n")
	    ch= int(input("Enter your choice: "))
	    
	    def remove_pattern(input_txt, pattern):
	            r = re.findall(pattern, input_txt)
	            for i in r:
	                input_txt = re.sub(i, '', input_txt)
	                
	            return input_txt 

	    def summarize1():
	        consumer_key= 'Ubtqpa8HQy0LNNQ1x2nakA5eO'
	        consumer_secret= 'DDlMdLMixGBDhDUTPVygSFm62AcXu71QHauAxrxszzENgDutZF'
	        access_token= '1237810270413586432-1aOwN2Al1tXD0MR5ZEtIuXO3H0ADgV'
	        access_token_secret= '62lFNz8zIpqlGgTwhjdKGUjaEJx2kKL78w0vIBHWQrf9c'
	        TOKEN = input("Enter your Access Token for Facebook Graph API Explorer: ")
	        auth = tw.OAuthHandler(consumer_key, consumer_secret)
	        auth.set_access_token(access_token, access_token_secret)
	        api = tw.API(auth, wait_on_rate_limit=True)
	        while True:
	            k1=0
	            k2=input("Do you want to extract tweets of a specific user/company handle?....(Yes/No)  ")
	            if(k2.lower()=="yes"):
	                # Define the search term and the date_since date as variables
	                sc = input("Enter the Screen Name of the Twitter handle: ")
	                n = int(input("Enter number of search terms :"))
	                search_words=[]
	                print("Enter the search terms:")
	                for i in range(0, n): 
	                    ele = input()
	                    search_words.append(ele)
	                n1=int(input("Enter the number of facebook posts and tweeets required for the data extraction: "))
	                date_since = input("Enter the date from when the tweets and facebook posts were made: ")
	                tweets = tw.Cursor(api.search,q=search_words,lang="en",since=date_since,tweet_mode='extended').items(n1)
	                a=[]
	                for tweet in tweets:
	                    if(tweet.user.screen_name==sc):
	                        print(tweet.full_text)
	                        if(tweet.full_text.startswith("RT @")==True):
	                            res = re.search('@(\w+)', tweet.full_text)
	                            tweet.full_text = re.sub(re.compile(r' I ',re.IGNORECASE),' @'+res.group(1)+' ',tweet.full_text)
	                            tweet.full_text = re.sub(re.compile(r" I'",re.IGNORECASE)," @"+res.group(1)+"'",tweet.full_text)
	                        else:
	                            tweet.full_text = re.sub(re.compile(r' I ',re.IGNORECASE),' @'+tweet.user.screen_name+' ',tweet.full_text)
	                            tweet.full_text = re.sub(re.compile(r" I'",re.IGNORECASE)," @"+tweet.user.screen_name+"'",tweet.full_text)
	                        #(tweet.text).replace(" I ",'@'+tweet.user.screen_name)
	                        #(tweet.text).replace("I ",tweet.user.screen_name)
	                        if tweet.full_text not in a:
	                            a.append(tweet.full_text)
	                
	            elif(k2.lower()=="no"):
	                # Define the search term and the date_since date as variables
	                n = int(input("Enter number of search terms :"))
	                search_words=[]
	                print("Enter the search terms:")
	                for i in range(0, n): 
	                    ele = input()
	                    search_words.append(ele)
	                n1=int(input("Enter the number of facebook posts and tweeets required for the data extraction: "))
	                date_since = input("Enter the date from when the tweets and facebook posts were made: ")
	                tweets = tw.Cursor(api.search,q=search_words,lang="en",since=date_since,tweet_mode='extended').items(n1)
	                a=[]
	                for tweet in tweets:
	                    #print(tweet.full_text)
	                    if(tweet.full_text.startswith("RT @")==True):
	                        res = re.search('@(\w+)', tweet.full_text)
	                        tweet.full_text = re.sub(re.compile(r' I ',re.IGNORECASE),' @'+res.group(1)+' ',tweet.full_text)
	                        tweet.full_text = re.sub(re.compile(r" I'",re.IGNORECASE)," @"+res.group(1)+"'",tweet.full_text)
	                    else:
	                        tweet.full_text = re.sub(re.compile(r' I ',re.IGNORECASE),' @'+tweet.user.screen_name+' ',tweet.full_text)
	                        tweet.full_text = re.sub(re.compile(r" I'",re.IGNORECASE)," @"+tweet.user.screen_name+"'",tweet.full_text)
	                    #(tweet.text).replace(" I ",'@'+tweet.user.screen_name)
	                    #(tweet.text).replace("I ",tweet.user.screen_name)
	                    if tweet.full_text not in a:
	                        a.append(tweet.full_text)
	            
	            else:
	                print("Invalid choice!!!")
	                k1=1
	            
	            if(k1==0):
	                break
	            
	        b=" ".join(a)
	        negations_ = {"isn't": "is not", "can't": "can not", "couldn't": "could not", "hasn't": "has not",
	                    "hadn't": "had not", "won't": "will not",
	                    "wouldn't": "would not", "aren't": "are not",
	                    "haven't": "have not", "doesn't": "does not", "didn't": "did not",
	                    "don't": "do not", "shouldn't": "should not", "wasn't": "was not", "weren't": "were not",
	                    "mightn't": "might not",
	                    "mustn't": "must not"}
	        neg_pattern = re.compile(r'\b(' + '|'.join(negations_.keys()) + r')\b')
	         
	        b = re.sub(re.compile(r'RT @'),'@',b)
	        b = re.sub(re.compile(r'\s{1,}|\t'),' ',b)
	        b = neg_pattern.sub(lambda x: negations_[x.group()], b)
	        b = b.replace("[^a-zA-Z]", "")
	        #b = re.sub(re.compile(r'\b(' + '|'.join(negations_.keys()) + r')\b'), repl=, string=b)
	        b = np.vectorize(remove_pattern)(b, r'@[\w]*:')
	        b = np.vectorize(remove_pattern)(b, r'#[\w]*:')
	        b = np.vectorize(remove_pattern)(b, r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))'r'[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})')
	        
	        #b = np.vectorize(remove_pattern)(b, r'[^a-zA-Z]')
	        
	        b = np.char.split(b, sep = '(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
	        #print(b)
	        sentences = []
	        for sentence in b.tolist():
	            #print(sentence)
	            sentence = sentence.strip()
	            sentence = re.sub(re.compile("[^0-9a-zA-Z -.,!@#$%^&*+=_;:']"),' ',sentence)
	            c=sentence.replace("[^0-9a-zA-Z]+", " ").split(" ")
	            c=list(filter(lambda a: a!='', c))
	            sentences.append(c)
	            
	        sentences1=[]
	        graph = facebook.GraphAPI(access_token=TOKEN, version="3.1")
	        posts = graph.search(q=search_words, type="place",fields='description',limit=n1,date=date_since)
	        for i in posts['data']:
	            for j in i:
	                if(j=='description'):
	                    sentences1.append(i[j])
	        #print(sentences1)
	        #print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
	        #print(" ".join(sentences[0])+" "+" ".join(sentences1))
	        
	                
	        def lda(sum2):
	            vect=CountVectorizer(ngram_range=(1,1),stop_words='english')
	            d=(sum2).split(". ")
	            dtm=vect.fit_transform(d)
	            lda=LatentDirichletAllocation(n_components=5)
	            lda_dtf=lda.fit_transform(dtm)
	            sorting=np.argsort(lda.components_)[:,::-1]
	            features=np.array(vect.get_feature_names())
	            mglearn.tools.print_topics(topics=range(5), feature_names=features,
	            sorting=sorting, topics_per_chunk=5, n_words=10)
	            Agreement_Topic=np.argsort(lda_dtf[:,2])[::-1]
	            #print("\nAgreement Topic:")
	            k=[]
	            for i in Agreement_Topic[:4]:
	                #print(".".join(d[i].split(".")[:2]) + ".\n")
	                k.append(".".join(d[i].split(".")[:2]) + ".\n")
	            #print("\n\nDomain Name Topic:")
	            Domain_Name_Topic=np.argsort(lda_dtf[:,4])[::-1]
	            for i in Domain_Name_Topic[:4]:
	                #print(".".join(d[i].split(".")[:2]) + ".\n")
	                if ".".join(d[i].split(".")[:2]) + ".\n" not in k:
	                    k.append(".".join(d[i].split(".")[:2]) + ".\n")
	            print("Summarized Text: ")
	            print(" ".join(k))
	            zit=pyLDAvis.sklearn.prepare(lda,dtm,vect)
	            pyLDAvis.show(zit,ip='127.0.0.1',port=8887)
	            d = path.dirname("")
	            alice_mask = np.array(Image.open(path.join(d, "Nigeria.png")))
	            stopwords = set(STOPWORDS)
	            wc = WordCloud(background_color="black", max_words=2000, mask=alice_mask,stopwords=stopwords)
	            wc.generate(sum2)
	            plt.figure(figsize=(16,13))
	            plt.imshow(wc, interpolation='bilinear')
	            plt.axis("off")
	            plt.figure()
	            plt.show()
	            
	    
	        print("\n\n\n\n")
	        lda(" ".join(sentences[0])+" "+" ".join(sentences1))
	        
	    
	    def summarize2():
	        n = int(input("Enter number of search terms :"))   
	        search_words=[]
	        print("Enter the search terms:")
	        for i in range(0, n): 
	            ele = input()
	            search_words.append(ele)
	        link=input("Enter the link for the xml format of RSS Feeds: ")
	        NewsFeed = feedparser.parse(link)
	        sentences=[]
	        for i in NewsFeed.entries:
	            #print(i.summary)
	            t=0
	            for i in NewsFeed.entries:
	                k=(i.summary).split(" ")
	                for j in search_words:
	                    for l in k:
	                        if(j.lower()==l.lower()):
	                            t=1
	                if(t==1):
	                    sentences.append(i.summary)
	         
	        
	        print("\n\n\n\n")
	        
	        #print(" ".join(sentences))

	        def lda():
	            vect=CountVectorizer(ngram_range=(1,1),stop_words='english')
	            d=" ".join(sentences).split(". ")
	            dtm=vect.fit_transform(d)
	            lda=LatentDirichletAllocation(n_components=5)
	            lda_dtf=lda.fit_transform(dtm)
	            sorting=np.argsort(lda.components_)[:,::-1]
	            features=np.array(vect.get_feature_names())
	            mglearn.tools.print_topics(topics=range(5), feature_names=features,
	            sorting=sorting, topics_per_chunk=5, n_words=10)
	            Agreement_Topic=np.argsort(lda_dtf[:,2])[::-1]
	            k=[]
	            #rint("\nAgreement Topic:")
	            for i in Agreement_Topic[:4]:
	                #print(".".join(d[i].split(".")[:2]) + ".\n")
	                k.append(".".join(d[i].split(".")[:2]) + ".\n")
	            #print("\n\nDomain Name Topic:")
	            Domain_Name_Topic=np.argsort(lda_dtf[:,4])[::-1]
	            for i in Domain_Name_Topic[:4]:
	                #print(".".join(d[i].split(".")[:2]) + ".\n")
	                if ".".join(d[i].split(".")[:2]) + ".\n" not in k:
	                    k.append(".".join(d[i].split(".")[:2]) + ".\n")
	            
	            print("Summarized Text: ")
	            print(" ".join(k))
	            zit=pyLDAvis.sklearn.prepare(lda,dtm,vect)
	            pyLDAvis.show(zit,ip='127.0.0.1',port=8887)
	            d = path.dirname("")
	            alice_mask = np.array(Image.open(path.join(d, "Nigeria.png")))
	            stopwords = set(STOPWORDS)
	            wc = WordCloud(background_color="black", max_words=2000, mask=alice_mask,stopwords=stopwords)
	            wc.generate(" ".join(sentences))
	            plt.figure(figsize=(16,13))
	            plt.imshow(wc, interpolation='bilinear')
	            plt.axis("off")
	            plt.figure()
	            plt.show()
	        
	        lda()

	    def ex():
	        p=1
	        return p
	        
	    def default():
	        print("Invalid choice!!")
	        return
	    
	    
	        
	    switcher1={1:summarize1,2:summarize2,3:ex}
	    def switch1(e):
	        p=switcher1.get(e,default)()
	        return p
	        
	    
	    p=switch1(ch)
	    if(p==1):
	        break