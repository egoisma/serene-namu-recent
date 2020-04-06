from flask import Flask
from flask_restful import Resource, Api
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import threading

app = Flask(__name__)
api = Api(app)

data_list = {'wiki': []}

def crawl(second=1.0):
	global data_list
	data_list = {'wiki': []}
	
	try:
		now = datetime.now(pytz.timezone('UTC'))
		
		sec = now.strftime('%S')

		URL = 'https://namu.wiki/RecentChanges'
		res = requests.get(URL)

		print('status:', res.status_code, now.strftime('%Y-%m-%d %H:%M:%S')[11:])
		html = res.text
		soup = BeautifulSoup(html, 'lxml')

		body = soup.body
		for tr in body.article.tbody.find_all('tr'):
			if(tr.td.a):

				# 여기서 지난 1분간의 모든 데이터를 시간 포함해서 다른 리스트에 저장해놓고
				# getData()에서 그 리스트의 값 중 지금 시간과 맞는 것을 data_list에 추가 후 전송하도록 바꾸기
				time_text = tr.find_all('td')[2].time.text
				if now.strftime('%Y-%m-%d %H:%M')[8:] == time_text[8:-3]:
					# 데이터 업데이트 후 크롤링 시 1초씩 늦어서 시간 매칭을 못 한다.
					# -> 현재 시간의 1~2초 전 데이터를 가져온다.
					if int(now.strftime('%S'))-2 == int(time_text[-2:]):
						print('->', tr.td.a.text, ',', int(tr.td.span.text[1:-1]))
						data_list['wiki'].append({'name':tr.td.a.text, 'size':int(tr.td.span.text[1:-1])})
		print()
	except Exception as ex:
		print(ex)
	
	threading.Timer(second, crawl, [second]).start()

class GetData(Resource):
	def get(self):
		print('data_list:',data_list)
		return data_list,  201, {'Access-Control-Allow-Origin': '*'}

if __name__ == '__main__':
	api.add_resource(GetData, '/data')
	app.run(host='0.0.0.0')

	crawl(1.0)
