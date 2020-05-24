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
import re
#importing libraries for pdf extraction
# Base library: pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
#importing libraries for text pre-processing
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
#importing libraries for summarization
from gensim import corpora
from gensim import models
from gensim import similarities
from gensim.summarization.summarizer import summarize



"""This function extracts text from PDFs present in a folder, named 'PDFs'.
Extracts text per paragraph"""
def pdf_to_text(path):
    text=[]
    resrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(resrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(resrcmgr, device)
    
    fp = open(path+".pdf", 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        layout = device.get_result()
        temp = []
        for ele in layout:
            #extracting text paragraph wise
            if isinstance(ele, LTTextBox):
                t = ele.get_text()
                if not t.isspace() and not len(t)==0:
                    temp.append(t)
        text.append(temp)
    fp.close()
    device.close()
    return text #returns overall extracted text

"""Preprocesses the text splitted into paragraphs. splitting each paragraph into tokens using tokeniser and 
removing stopwords as well as reducing words to their base forms."""
def preprocess_pdf(doc):
    global sent
    pattern = re.compile('\n+')
    sent_tokenizer = PunktSentenceTokenizer()
    texts = ''
    for j in doc:
        for i in j:
            raw = pattern.sub(' ',i)
            raw = sent_tokenizer.tokenize(raw)
            t=[]
            for k in raw:
                if k[-1]=='.':
                    t.append(k+" ")
            temp = ''.join(t)
            if len(temp)!=0:
                texts+=temp
    return texts
    
"""Extracting and reading data from pdf file"""   
def extract():
    doc = pdf_to_text(input("Enter the path of the file: "))   
    print ('Reading files...')
    data = preprocess_pdf(doc)
    return data
        
"""Pre_processing extracted data"""
def pre_process(doc):
    lemmatizer = WordNetLemmatizer()
    stop = stopwords.words('english')
    text=nltk.sent_tokenize(doc)
    tokens = [[word for word in nltk.word_tokenize(sent)] for sent in text ]
    tokens= [[w for w in sent if w not in stop] for sent in tokens]
    tokens = [[w.lower() for w in sent if w.isalpha()] for sent in tokens ]
    #stems = [[stemmer.stem(t) for t in sent] for sent in tokens]
    lemma = [[lemmatizer.lemmatize(t) for t in sent] for sent in tokens]
    return lemma

def rank(text):
    my_list=summarize(text,ratio=0.8).split('\n')
    return list(my_list)
    
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
def pdf_driver():
    #Extracting data
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



