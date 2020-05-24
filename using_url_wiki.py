#Author: Raunak Jain

#Sample input: https://www.mayoclinic.org/diseases-conditions/coronavirus/expert-answers/novel-coronavirus/faq-20478727

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
#from urllib.request import urlopen
from gensim.summarization import summarize
import wikipedia
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

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
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
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
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
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
        
    print("[+] Total External links:", len(external_urls))
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total:", len(external_urls) + len(internal_urls))

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
    
    print("Your summary is: ")
    
    summ1 = (summarize(article, word_count = wc)).split(".")
    final_sum = ""
    for sent in summ1:
        if("\n" in sent):
            sent = sent.replace("\n", "")
        sent = sent.strip()
        final_sum+=sent+". "
    print(final_sum)

def driver_wiki(topic, wc=1000):
    # Get wiki content. 
    wikisearch = wikipedia.page(topic) 
    article = wikisearch.content 
    summ1 = (summarize(article, word_count = wc)).split(".")
    final_sum = ""
    for sent in summ1:
        if("\n" in sent):
            sent = sent.replace("\n", "")
        sent = sent.strip()
        final_sum+=sent+". "
    print(final_sum)

def url_driver():
    print("\nSelect the desired option : ")
    print("1. Using URL")
    print("2. Using Wikipedia\n")
    n = int(input())


    if(n==1):
        url = input("Please enter the url: ")
        depth = int(input("Please enter the depth: "))
        k = int(input("Please enter the number of keywords: "))
        keywords=[]
        print("\nPlease enter the keywords one by one: ")
        for i in range(k):
            key = input("Enter keyword {} : ".format(i+1))
            keywords.append(key.strip())
        print(keywords)
        wc = 1000
        wc = int(input("Please enter the number of words to generate: "))
        driver_bs(url, keywords, depth, wc)
    elif(n==2):
        topic = input("Please enter the topic: ")
        wc = 10
        wc = int(input("Please enter the number of words to generate: "))
        driver_wiki(topic, wc)
    
    
    