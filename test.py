import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import threading
end=False
def crawl(second=1.0):
    global end
    if end:
        return
    now = datetime.now(pytz.timezone('UTC'))
    URL = 'https://namu.wiki/RecentChanges'
    res = requests.get(URL)

    print(res.status_code)
    print()
    html = res.text
    soup = BeautifulSoup(html, 'lxml')

    body = soup.body

    for tr in body.article.tbody.find_all('tr'):
        if(tr.td.a):
            if now.strftime('%Y-%m-%d %H:%M:%S')[8:] == tr.find_all('td')[2].time.text[8:]:
                print(tr.td.a.text, tr.find_all('td')[2].time.text[8:])
    print()

    threading.Timer(second, crawl, [second]).start()

crawl(1)