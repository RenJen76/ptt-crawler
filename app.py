import os
import Crawler
from LineNotify import LineNotify

if __name__ == "__main__":

    message     = '基本功能測試!!'
    # Craw        = Crawler.Crawler()
    # print(Craw.callRequest('Lifeismoney'))
    LineNotify  = LineNotify()
    # print(LineNotify.token)
    LineNotify.NotifyMessage(message)
