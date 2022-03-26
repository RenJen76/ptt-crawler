import os
import Crawler
from LineNotify import LineNotify

if __name__ == "__main__":

    lineNotify  = LineNotify() 
    craw        = Crawler.Crawler('multiple')
    crawResult  = craw.startCrawler()

    for article in crawResult:
        if article.get('comment') > 20:
            lineNotify.NotifyMessage('【'+str(article.get('comment'))+'】'+article.get('title')+' '+article.get('href'))