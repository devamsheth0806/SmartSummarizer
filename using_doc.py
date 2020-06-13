#importing libraries of general usage
import nltk

#importing libraries for text pre-processing
from nltk.stem import WordNetLemmatizer
from collections import defaultdict

#importing libraries for summarization
from gensim import corpora
from gensim import models
from gensim import similarities
from gensim.summarization.summarizer import summarize
import sys

"""Extracting and reading data from .txt file"""    
def extract(link):
    docs=open(link,'r',errors='ignore').read()
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
def lsi_sum(texts, documents,keywords,sent):
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    #Detecting the topics
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=5)

    #query=input("Enter the keywords: ")
    query = " ".join(keywords)
    vec_bow = dictionary.doc2bow(query.lower().split())
    
    # convert the query to LSI space
    vec_lsi = lsi[vec_bow]  
    
    #Cosine similarity between query and lsi model
    index = similarities.MatrixSimilarity(lsi[corpus])
        
    sims = index[vec_lsi]  # perform a similarity query against the corpus
    
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    
    sent=sent*10/8
    final=""
    for i, s in enumerate(sims):
        if(sent>0):
            final=final+documents[s[0]]+" "
            sent=sent-1
    my_list=rank(final)
    final=""
    lower=['these','those','this','that']
    upper=['This', 'That','These','Those']
    for s in lower:
        my_list[0]=my_list[0].replace(s,"the")
    for s in upper:
        my_list[0]=my_list[0].replace(s,"The")
    for sent in my_list:
        final=final+sent+" "
    return final

"""driver function for summarizing text files"""
def doc_driver(path,keywords,sent):
    
    #Extracting data from given file based on type
    docs=extract(path)

    documents=nltk.sent_tokenize(docs)
    texts=pre_process(docs)
    
    #remove words that appear only once
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    # texts = [[token for token in text if frequency[token] > 2] for text in texts]
    keywords=keywords.splitlines()
    for i in keywords:
        i=i.strip()
    #Summarisation using LSI model and gensim summarizer
    final=lsi_sum(texts, documents,keywords,int(sent))
    print(final)

doc_driver(sys.argv[1],sys.argv[2],sys.argv[3])