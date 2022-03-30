import requests
import json
import time
import threading
import pprint
import configparser
from loguru import logger
from bs4 import BeautifulSoup 

class Crawler:

    domain      = "https://www.ptt.cc"
    crawlerType = ""
    allThreads  = []
    threadResult= {}

    def __init__(self, crawlerType = ''):

        config = configparser.ConfigParser()
        config.read('config/config.ini')
        self.crawlerType    = crawlerType
        self.loadPage       = int(config['NORMAL'].get('loadPage', 1))

    def crawlerIndex(self, channel = 'Lifeismoney'):

        articles    = []
        requestUrl  = self.domain + "/bbs/" + channel + "/index.html"

        for _ in range(0, self.loadPage):
            logger.info('GET: ' + requestUrl)
            articles    = articles + self.startCrawler(requestUrl)
            sendRequest = requests.get(requestUrl)
            soup        = BeautifulSoup(sendRequest.text,"html.parser")
            getLastPage = soup.select(".btn.wide:nth-child(2)")
            if len(getLastPage) != 1:
                logger.error('無法取得索引頁面('+requestUrl+')')
                break;
            requestUrl  = self.domain + getLastPage[0].get('href')
        return articles

    def crawlerPage(self, crawlerUrl):

        index       = 0
        sendRequest = requests.get(crawlerUrl)
        soup        = BeautifulSoup(sendRequest.text,"html.parser")
        articles    = soup.select("div.r-ent")
        result      = []

        for article in articles:
            data    = {}
            title   = article.select(".title a")
            if len(title) > 0:

                data["author"]  = article.select(".author")[0].text
                data["date"]    = article.select(".date")[0].text
                data["href"]    = self.domain + "/" + title[0]["href"]
                data["title"]   = title[0].text

                if self.crawlerType=="multiple":
                    thread = threading.Thread(target=self.crawlerArticle, args=(title[0]["href"],index,))
                    thread.start()
                    self.allThreads.append(thread)
                else:
                    data["comment"] = self.crawlerArticle(title[0]["href"])

                result.insert(index, data)
                index = index + 1

        return result
        # return json.dumps(result).encode().decode('unicode_escape')

    def crawlerArticle(self, url, index = ''):
        sendRequest     = requests.get(self.domain + url)
        soup            = BeautifulSoup(sendRequest.text,"html.parser")
        articlesCount   = len(soup.find_all("div", {"class": "push"}))
        if self.crawlerType=="multiple":
            self.threadResult[index] = articlesCount
        else:
            return articlesCount 

    def startCrawler(self, crawlerUrl):
        start_time  = time.time()
        index       = self.crawlerPage(crawlerUrl)

        if self.crawlerType=="multiple":
            for t in self.allThreads:
                t.join()
            for key, comments in self.threadResult.items():
                index[key]['comment'] = comments
        end_time = time.time()
        logger.info(f"{end_time - start_time} 秒爬取 {len(index)} 頁的文章")
        return index