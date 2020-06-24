import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
#from urllib.request import urlopen
from gensim.summarization import summarize
import wikipedia
import sys
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import random
# init the colorama module
#We are going to use colorama just for using different colors when printing, to distinguish between internal and external links
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    urls.add(url)
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content,features="lxml")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
                # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                #print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        #print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls

# number of urls visited so far will be stored here
total_urls_visited = 0

def crawl(url, max_urls=2):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 50.
    """
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

def driver_bs(url, keywords, depth=0, wc=1000):
    if(depth==0):
        internal_urls.add(url)
    elif(depth==1):
        internal_urls.add(url)
        get_all_website_links(url)
    else:
        internal_urls.add(url)
        crawl(url, depth)

    article=""
    page = requests.get(url).text
    soup = BeautifulSoup(page, features="lxml")    
    p_tags = soup.find_all('p')
    p_tags_text = [tag.get_text().strip() for tag in p_tags]
    sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]
    sentence_list = [sentence for sentence in sentence_list if '.' in sentence]
    for i in range(len(sentence_list)-1):
        if(i>=len(sentence_list)):
            break
        for key in keywords:
            if(key.lower() in sentence_list[i].lower()):
                article += sentence_list[i]
                #article += sentence_list[i+1]
                break
    if(url in internal_urls):
        internal_urls.remove(url)
    
    #Preprocessing
    for url in internal_urls:
        page = requests.get(url).text
        soup = BeautifulSoup(page, features="lxml")    
        p_tags = soup.find_all('p')
        p_tags_text = [tag.get_text().strip() for tag in p_tags]
        sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]
        sentence_list = [sentence for sentence in sentence_list if '.' in sentence]
        for i in range(len(sentence_list)-1):
            if(i>=len(sentence_list)):
                break
            for key in keywords:
                if(key.lower() in sentence_list[i].lower()):
                    article += sentence_list[i] + " " + sentence_list[i+1]
                    i+=1
                    break
    
    summ1 = (summarize(article, word_count = wc)).split(".")
    final_sum = ""
    for sent in summ1:
        if("\n" in sent):
            sent = sent.replace("\n", "")
        sent = sent.strip()
        final_sum+=sent+". "
    return final_sum

def driver_wiki(topic, wc=1000):
    # Get wiki content. 
    try:
        wikisearch = wikipedia.page(topic) 
    except wikipedia.DisambiguationError as e:
        for top in e.options:
            try:
                wikisearch=wikipedia.page(top)
                break
            except:
                pass
    article = wikisearch.content 
    summ1 = (summarize(article, word_count = wc)).split(".")
    final_sum = ""
    for sent in summ1:
        if("\n" in sent):
            sent = sent.replace("\n", "")
        sent = sent.strip()
        final_sum+=sent+". "
    #print(final_sum)
    return final_sum

def url_driver(path,keywords,depth1,noword,n):
    
    if(n=='1'):
        url = path
        depth = int(depth1)
        keywords=keywords.splitlines()
        for i in keywords:
            i=i.strip()
        wc=int(noword)
        #try:
        final_sum = driver_bs(url, keywords, depth, wc)
        """except:
            final_sum = Connection Error or Keyword error"""
        print(final_sum)
        
    elif(n=='2'):
        keywords=keywords.splitlines()
        for i in keywords:
            i=i.strip()
        topic = "".join(keywords)
        wc = int(noword)
        try:
            final_sum = driver_wiki(topic, wc)
        except:
            final_sum = "Connection Error or Keyword error"
        print(final_sum)

url_driver(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])