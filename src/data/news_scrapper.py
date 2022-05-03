# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 21:18:35 2022

@author: krish
"""

from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import json, xml
import requests
import html
import re 
import xml.etree.ElementTree 
import itertools
import os, tempfile, gcsfs
import newspaper
import pathlib
abspath = pathlib.Path(__file__).parent.resolve()



# Writing data to GCP bucket
def writeDataToCloud(company, news_list):
    # Initializing GCSFS 
    project_name = 'big-data-final-project'
    credentials = os.path.join(abspath,"big-data-final-project-347804-0935c4105776.json")
    # credentials = "big-data-final-project-347804-0935c4105776.json"
    FS = gcsfs.GCSFileSystem(project=project_name, token=credentials)
    try:
        # Write to temp file
        temp = tempfile.NamedTemporaryFile(delete=False,mode='w',suffix='.txt') 
        with open(temp.name, "w", encoding="utf-8") as output:
            output.write(str((news_list)))
        # Upload to GCP bucket
        FS.upload(temp.name, f'stock_news/{company}.txt')
        temp.close()
        os.unlink(temp.name)
        # returning the url for the location
        return FS.url(f'stock_news/{company}.txt').replace('googleapis','cloud.google')
    except Exception as e:
        raise Exception(f'Output Error: Error writing data to Google Cloud Bucket {e}')
  
# De-contracting english phrases
def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return str(phrase)

def clean_text(text):
    #Clean the html tags 
    text = html.unescape(text)
    
    # remove hyperlinks
    text = re.sub(r'https?:\/\/.\S+', "", text)
    
    # remove hashtags
    # only removing the hash # sign from the word
    text = re.sub(r'#', '', text)
    text = re.sub(r'\"', '', text)
    text = re.sub(r'’','\'',text)
    text = re.sub(r'”','',text)
    text = re.sub(r'“','',text)
    
    # remove old style retweet text "RT"
    text = re.sub(r'^RT[\s]+', '', text)
    
    #One letter in a word should not be present more than twice in continuation
    text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
    
    return decontracted(text)
    
# Remove tags (https://stackoverflow.com/questions/19369901/python-element-tree-extract-text-from-element-stripping-tags)
# def remove_tags(text):
#     return ''.join(xml.etree.ElementTree.fromstring(text).itertext())

def remove_tags(text):
    try:
        output = ''.join(xml.etree.ElementTree.fromstring(text).itertext())
    except Exception:
        output = text
    return output

def basicScrapper(url):
    try:
        article = newspaper.Article(url=url, language='en')
        article.download()
        article.parse()
    except Exception as e:
        print(f'Error in Basic Scrapper using NewsPaper3K: {e}')
        return ''
    return str(article.text)

# Function to scrape news
def getNews(company, writeCloud=False, proxies=''):
    
    
    # Generate 5 API keys from https://newsapi.org/register
   
    keys = [apikey1,apikey2,apikey3,apikey4,apikey5]
    for i in range(len(keys)):
        try:
            key = keys[i]
            print(f'Trying API Key {i+1} for NewsAPI request: {key}')
            newsapi = NewsApiClient(api_key = key)
            news = newsapi.get_top_headlines(category='business', language='en')
            break
        except Exception as e:
            if not e.args[0]['code'] == 'rateLimited':
                raise Exception(f'NewsAPI Error!! {e}')
            



    # Remove whitespaces from parameter
    company = company.strip()
    # Setting keywords for query
    queries = ['Stock', 'Investors', 'Profits', 'Finances', 'Performance', '']
    # Output objects
    output_obj = []
    titles = []
    # Get top headlines for each subquery of the company
    print('Started Top Business Headlines Srapping!')
    for query in queries:
        news = newsapi.get_top_headlines(q=(company+' '+query).strip(), category='business', language='en')
        # Get unique articles, limit to 10 articles
        for article in news['articles']:
            if article['title'] not in titles and company.lower() in article['title'].lower():
                # Delete unused keys
                del article['source'], article['author'], article['urlToImage']
                if len(titles) == 10:
                    break
                article['content'] = getFullArticleContent(company=company, url = article['url'], pre_content = article['content'], proxies=proxies)
                # ONLY append articles to output object if article content and description are not empty
                if len(article['content'])!= 0 and len(article['description'])!= 0:
                    output_obj.append(article)
                    titles.append(article['title'])
    
    # If headlines <10 -> Get all news articles with the company name as keyword
    if not len(titles) == 10:
        print('Started Full News Srapping!')
        news = newsapi.get_everything(q=(company).strip(), language='en')
        for article in news['articles']:
            if article['title'] not in titles and company.lower() in article['title'].lower():
                del article['source'], article['author'], article['urlToImage']
                if len(titles) == 10:
                    break
                article['content'] = getFullArticleContent(company=company, url = article['url'], pre_content = article['content'], proxies=proxies)
                if len(article['content'])!= 0 and len(article['description'])!= 0:
                    output_obj.append(article)
                    titles.append(article['title'])
    
    # If total news are still < 10 -> Get all news with out getting custom full content.
    if not len(titles) == 10:
        print('Started Basic Srapping!')
        for article in news['articles']:
            if len(titles) == 10:
                break
            if article['title'] not in titles and company.lower() in article['title'].lower():
                content = basicScrapper(article['url'])
                if len(content) == 0:
                    article['content'] = clean_text(remove_tags(article['content'].split('… [')[0]))
                else:
                    article['content'] = content
                # article['content'] = clean_text(article['content'].split('… [')[0])
                if len(article['content'])!= 0 and len(article['description'])!= 0:
                    output_obj.append(article)
                    titles.append(article['title'])
            
    # Summary
    try:
        # For all articles, concatenate title, description, content into one, use as input for summarization API
        for article in output_obj:
            article['content'] = article['title']+' '+article['description']+' '+article['content']
            # Lambda function for summarization
            response = requests.post("https://j3btan6btg.execute-api.us-east-1.amazonaws.com/dev/summary", json = article)
            if response.status_code == 200:
                if not 'news_summary' in response.json().keys():
                    raise Exception(f"Error in Summarization {response.json()}")
                article['summary'] = response.json()['news_summary']
            else:
                raise Exception(f"Lambda Function Error. Not a 200 status code response!: {response.json()}")
    except Exception as e:
        raise Exception(f"Error in Summarization {e}")
    
    # Sentiment
    try:
        # For all articles, concatenate title, description, content into one, use as input for summarization API
        for article in output_obj:
            article['content'] = article['title']+' '+article['description']+' '+article['summary']
            # Lambda function for summarization
            response = requests.post("https://n9h06pjw6f.execute-api.us-east-1.amazonaws.com/dev/sentiment", json = article)
            if response.status_code == 200:
                if not 'sentiment' in response.json().keys():
                    raise Exception(f"Error in Sentiment Analysis {response.json()}")
                article['sentiment'] = response.json()['sentiment']
            else:
                raise Exception(f"Lambda Function Error. Not a 200 status code response!: {response.json()}")
    except Exception as e:
        raise Exception(f"Error in Sentiment Analysis {e}")
    
    if writeCloud:
        url = writeDataToCloud(company, output_obj)
        return url
    return titles, output_obj


def getFullArticleContent(company, url, pre_content='', proxies=''):
    if not pre_content:
        pre_content=''
    content = ''
    # Request
    try:
        response = requests.get(url, proxies=proxies)
    except Exception:
        print(f'URL not reachable: {url}')
        return ''
    # Successful request
    if response.status_code == 200:
        # Fetch content from website
        body = response.content
        # BeautifulSoup object creation
        soup1 = BeautifulSoup(body, 'html.parser')
        # Get all the script type contents from the html code of the article main page (This is the design for EconomicTimes)
        news = soup1.find_all('script')
        
        for article in news:
            try:
                if article.has_attr('type'):
                    # The article is stored in json format
                    if 'json' in article['type']:
                        obj = json.loads(article.contents[0])
                        #NewsArticle is the @type key's value in the json
                        if '@type' in obj.keys():
                            if obj['@type'] ==  'NewsArticle':
                                # articleBody is the key for the article in the json
                                content+=' '+ str(obj["articleBody"])
            except Exception:
                pass
            
        # This is for the format how US blogs write their articles in div class
        news_div = soup1.find_all('div')
        for div in news_div:
            try:
                paras = div.find_all('p')
                for para in paras:
                    data = str(remove_tags(str(para)))
                    # Check if article content is unique
                    if company.lower() in data.lower() and data.lower() not in content.lower():
                        content+=' '+data
            except Exception:
                pass
            
        # If content is empty     
        if len(content) == 0:
            # This is for the format how US blogs write their articles in div class
            news_div = soup1.find_all('div', class_='article-text')
            for article in news_div:
                try:
                    #removing all html tags from the content
                    content+=' '+ str(remove_tags(str(article)))
                except Exception:
                    pass
            
            # This is for the format how US blogs write their articles in div class
            news_div = soup1.find_all('div', class_='article-content')
            for article in news_div:
                try:
                    paragraphs = article.find_all('p')
                    for para in paragraphs:
                    #removing all html tags from the content
                        content+=' '+ str(remove_tags(str(para)))
                except Exception:
                    pass
            
            # This is for the format how US blogs write their articles in div class
            news_div = soup1.find_all('div', class_='entry-content clearfix')
            for article in news_div:
                try:
                    paragraphs = article.find_all('p')
                    for para in paragraphs:
                    #removing all html tags from the content
                        content+=' '+ str(remove_tags(str(para)))
                except Exception:
                    pass
    else:
        content= '' 
    if len(content) == 0:
        content = ''
    
    return clean_text(content)

# getNews for all companies on a daily basis
def getAllNews():
    companies = ['Apple','Microsoft','Amazon','Walmart','Alphabet','Meta','Tesla','NVIDIA','Pfizer','Netflix']
    urls = []
    for company in companies:
        try:
            url = getNews(company=company,  writeCloud=True)
            
        except Exception as e:
            if 'rateLimited' in str(e):
                url = getNews(company=company,  writeCloud=True)
            else:
                raise Exception(f'Error in {company} Company due to Error: {e}')
            
        print(url)
        urls.append(url)
        
    return urls
    
if __name__=='__main__':
    # Generate an API key from https://newsapi.org/register
    companies = ['Apple','Microsoft','Amazon','Walmart','Alphabet','Meta','Tesla','NVIDIA','Pfizer','Netflix']
    for company in companies:
        url = getNews(company=company,  writeCloud=True)
        print(url)

   
