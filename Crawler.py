import requests
import json
import time
import threading
import pprint
from queue import Queue
from bs4 import BeautifulSoup 

class Crawler:

    domain      = "https://www.ptt.cc"
    crawlerType = ""
    allThreads  = []
    threadResult= {}

    def __init__(self, crawlerType = ''):

        self.crawlerType    = crawlerType
        self.queue          = Queue()

    def crawlerIndex(self, channel = 'MobileComm'):

        index       = 0
        sendRequest = requests.get(self.domain + "/bbs/" + channel + "/index.html")
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

    def startCrawler(self):
        start_time  = time.time()
        index       = self.crawlerIndex('Lifeismoney')

        if self.crawlerType=="multiple":
            for t in self.allThreads:
                t.join()
            for key, comments in self.threadResult.items():
                index[key]['comment'] = comments
        return index
        # end_time = time.time()
        # pprint.pprint(index)
        # print(f"{end_time - start_time} 秒爬取 {len(index)} 頁的文章")