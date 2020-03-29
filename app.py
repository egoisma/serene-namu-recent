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
    
	sec = now.strftime('%S')

	URL = 'https://namu.wiki/RecentChanges'
	res = requests.get(URL)

	print('status:', res.status_code, now.strftime('%Y-%m-%d %H:%M:%S')[11:])
	html = res.text
	soup = BeautifulSoup(html, 'lxml')

	body = soup.body
	data_list = dict()
	for tr in body.article.tbody.find_all('tr'):
		if(tr.td.a):
			# 데이터 업데이트 후 크롤링 시 1초씩 늦어서 시간 매칭을 못 한다.
			# -> 현재 시간의 1~2초 전 데이터를 가져온다.
			time_text = tr.find_all('td')[2].time.text
			if now.strftime('%Y-%m-%d %H:%M')[8:] == time_text[8:-3]:
				if int(now.strftime('%S'))-2 == int(time_text[-2:]):
					print('->', tr.td.a.text, ',', int(tr.td.span.text[1:-1]))
					data_list[tr.td.a.text] = int(tr.td.span.text[1:-1])
	print()
	return data_list

class GetData(Resource):
	def get(self):
		data_list = crawl()
		print('datalist',data_list)
		#return {'status': 'success'},  201, {'Access-Control-Allow-Origin': '*'}
		return data_list,  201, {'Access-Control-Allow-Origin': '*'}
api.add_resource(GetData, '/data')

if __name__ == '__main__':
    app.run(debug=False)
