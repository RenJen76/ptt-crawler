import requests
import json
from bs4 import BeautifulSoup 

class Crawler:

    domain = "https://www.ptt.cc/bbs"

    def callRequest(self, channel = 'MobileComm'):
        sendRequest = requests.get(self.domain + "/" + channel + "/index.html")
        soup        = BeautifulSoup(sendRequest.text,"html.parser")
        articles    = soup.select("div.r-ent")
        result      = []

        for article in articles:
            data    = {}
            title   = article.select(".title a")
            if len(title) > 0:
                data["author"]  = article.select(".author")[0].text
                data["date"]    = article.select(".date")[0].text
                data["href"]    = title[0]["href"]
                data["title"]   = title[0].text
                result.append(data)
            
        return json.dumps(result).encode().decode('unicode_escape')