# -*- coding: utf-8 -*-
"""
Created on Fri May  8 01:44:16 2020

@author: Samridhi
"""
#importing libraries of general usage
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
#importing libraries for text pre-processing
from nltk.stem import WordNetLemmatizer
from collections import defaultdict

#importing libraries for summarization
from gensim import corpora
from gensim import models
from gensim import similarities
from gensim.summarization.summarizer import summarize

"""Extracting and reading data from .txt file"""    
def extract():
    path = input('Please Enter Directory Path: ')
    print ('Reading files...')
    file = path+".txt"
    docs=open(file,'r',errors='ignore').read()
    return docs
           
"""Pre_processing extracted data"""
def pre_process(doc):
    lemmatizer = WordNetLemmatizer()
    stopwords = nltk.corpus.stopwords.words('english')
    text=nltk.sent_tokenize(doc)
    tokens = [[word for word in nltk.word_tokenize(sent)] for sent in text ]
    tokens= [[w for w in sent if w not in stopwords] for sent in tokens]
    tokens = [[w.lower() for w in sent if w.isalpha()] for sent in tokens ]
    #stems = [[stemmer.stem(t) for t in sent] for sent in tokens]
    lemma = [[lemmatizer.lemmatize(t) for t in sent] for sent in tokens]
    return lemma

"""Level two summarization- taking 0.8 percent of level 1 summarizer and sentence ranking applied"""
def rank(text):
    my_list=summarize(text,ratio=0.8).split('\n')
    return list(my_list)
    
"""This function is used for: 
Topic Modelling using LSI
Incorporating the query given to find most similar sentences
Level 1 summarization - cosine similarity matrix"""
def lsi_sum(texts, documents):
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    #Detecting the topics
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=5)
    
    #Printing topic wise keywords discussed
    check=int(input("View keywords of topics discussed: \nPress 1 for Yes\nPress 0 for No\n"))
    if(check==1):
        print("\nTopic wise keywords are:")
        for index, topic in lsi.show_topics(formatted=False, num_words= 10):
            print('Topic: {} \nWords: {}'.format(index, [w[0] for w in topic]))

    query=input("Enter the keywords: ")
    vec_bow = dictionary.doc2bow(query.lower().split())
    
    # convert the query to LSI space
    vec_lsi = lsi[vec_bow]  
    
    #Cosine similarity between query and lsi model
    index = similarities.MatrixSimilarity(lsi[corpus])
        
    sims = index[vec_lsi]  # perform a similarity query against the corpus
    # print (document_number, document_similarity) 2-tuples)
    #print(list(enumerate(sims)))
    
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    sent=int(input("Enter the number of sentences required: "))
    sent=sent*10/8
    final=""
    for i, s in enumerate(sims):
        if(sent>0):
            final=final+documents[s[0]]+" "
            sent=sent-1
    my_list=rank(final)
    final=""
    for sent in my_list:
        final=final+sent+" "
    return final

"""Main function"""
def doc_driver():
    #Extracting data from given file based on type
    docs=extract()
    
    #preprocessing files
    print ("Preprocessing data extracted...")
    documents=nltk.sent_tokenize(docs)
    texts=pre_process(docs)
    
    #remove words that appear only once
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    # texts = [[token for token in text if frequency[token] > 2] for text in texts]
            
    #Summarisation using LSI model and gensim summarizer
    final=lsi_sum(texts, documents)
    print("\nThe required summary is: ")
    print(final)



