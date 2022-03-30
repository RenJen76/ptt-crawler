import os
import Crawler
import configparser
from loguru import logger
from LineNotify import LineNotify

if __name__ == "__main__":

    logger.add('log.txt', rotation="1 week")
    userConfig = configparser.ConfigParser()
    userConfig.read('config/config.ini')
    notificationLimit = int(userConfig['NORMAL'].get('notificationLimit', 10))

    lineNotify  = LineNotify() 
    craw        = Crawler.Crawler('multiple')
    crawResult  = craw.crawlerIndex()

    for article in crawResult:
        if article.get('comment') > notificationLimit:
            lineNotify.NotifyMessage('【'+str(article.get('comment'))+'】'+article.get('date')+' '+article.get('title')+' '+article.get('href'))