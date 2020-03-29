import requests
from bs4 import BeautifulSoup

URL = 'https://namu.wiki/RecentChanges'
res = requests.get(URL)

print(res.status_code)
print()
html = res.text
soup = BeautifulSoup(html, 'lxml')

body = soup.body

for tr in body.article.tbody.find_all('tr')[:15]:
    if(tr.td.a):
        print(tr.td.a.text)
