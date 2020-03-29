from flask import Flask
from flask_restful import Resource, Api
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

app = Flask(__name__)
api = Api(app)

def crawl():
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

class GetData(Resource):
    def get(self):
		data_list = crawl()

    	return {'status': 'success'},  201, {'Access-Control-Allow-Origin': '*'}

api.add_resource(GetData, '/get')

if __name__ == '__main__':
    app.run(debug=True)
