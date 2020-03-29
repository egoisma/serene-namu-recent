import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import threading

end=False
sec=0;
def crawl(second=1.0):
    global end, sec
    if end:
        return
    
    now = datetime.now(pytz.timezone('UTC'))
    
    if sec != now.strftime('%S'):
        sec = now.strftime('%S')

        URL = 'https://namu.wiki/RecentChanges'
        res = requests.get(URL)

        print('status:', res.status_code, now.strftime('%Y-%m-%d %H:%M:%S')[11:])
        html = res.text
        soup = BeautifulSoup(html, 'lxml')

        body = soup.body
        #if(body.article.tbody.find_all('tr')[0].td.a):
        #    print('0->', body.article.tbody.find_all('tr')[0].td.a.text, body.article.tbody.find_all('tr')[0].find_all('td')[2].time.text[8:])
        for tr in body.article.tbody.find_all('tr'):
            if(tr.td.a):
                # 데이터 업데이트 후 크롤링할 때 1초씩 늦어서 시간 매칭을 못 한다.
                if now.strftime('%Y-%m-%d %H:%M:%S')[8:] == tr.find_all('td')[2].time.text[8:]:
                    print('->', tr.td.a.text)

    threading.Timer(second, crawl, [second]).start()

# 
crawl(0.5)