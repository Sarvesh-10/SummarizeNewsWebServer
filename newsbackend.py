from flask import Flask,render_template
import requests
from textblob import TextBlob
import nltk
import json
from newsapi.newsapi_client import NewsApiClient


from newspaper import Article
nltk.download('punkt')
Newsapi = NewsApiClient(api_key='cc10ab289d7a4bfaae76a9874cd6ee43')


class News:
    author = ''
    publishDetails =''
    title = ''
    url = ''
    urlToImage = ''
    summarizeNews = ''
    def __init__(self,author,publishDetails,title,url,urlToImage):
        self.author = author
        self.publishDetails = publishDetails
        self.title = title
        self.url = url
        self.urlToImage = urlToImage
    






app = Flask(__name__)

def formData(newsData):
    listOfNews = []
    for article in newsData['articles']:
        listOfNews.append(News(author=article['author'],publishDetails=article['publishedAt'],title=article['title'],url=article['url'],urlToImage=article['urlToImage']))
    return listOfNews


def summarize(listOfNews):
    for news in listOfNews:
        article = Article(news.url)
        article.download()
        article.parse()
        article.nlp()
        news.summarizeNews = article.summary
    return listOfNews


        
        

@app.route('/<cat>')
def getNews(cat):
    newsData = Newsapi.get_top_headlines(language='en',country='in',category=cat)
    print(type(newsData))
    listOfNews = formData(newsData=newsData)
    listOfNews = summarize(listOfNews=listOfNews)
    jsonString =  json.dumps(listOfNews,default=lambda o:o.__dict__)
    return jsonString

@app.route('/')
def index():
    return "<h1>Add /sports or /business or /general or /health or /technology or /science</h1>"
    
    


if __name__ == "__main__":
    app.run(debug=True)



'''
1. categories
    i) general
    ii)Sports
    iii)Business
    iv)Entertainment
    v)Health

    

    ix)science
    x)Technology

    
    
    xiv)general
'''



        


