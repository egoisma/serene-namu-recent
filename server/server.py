from flask import Flask
from flask_restful import Resource, Api
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import threading

app = Flask(__name__)
api = Api(app)


data_list = {'wiki': []}  # 현재시간으로부터 delay 전까지의 크롤링 데이터를 담는다.

DELAY = 10.0
def crawl(delay=DELAY):
	global data_list
	data_list = {'wiki': []}
	
	try:
		now = datetime.now(pytz.timezone('UTC'))

		URL = 'https://namu.wiki/RecentChanges'
		res = requests.get(URL)

		print('crawl status:', res.status_code, now.strftime('%Y-%m-%d %H:%M:%S')[11:])
		html = res.text
		soup = BeautifulSoup(html, 'lxml')

		body = soup.body
		for tr in body.article.tbody.find_all('tr'):
			if(tr.td.a):
				# 지난 delay 시간 동안의 모든 데이터를 시간 포함해서 data_list에 저장함
				time_text = tr.find_all('td')[2].time.text
				if now.strftime('%Y-%m-%d %H:%M')[8:] == time_text[8:-3]: # match day, hour, and minute

					# 현재 시간부터 현재 시간의 delay(초) 전까지의 데이터를 불러옴
					if int(now.strftime('%S'))-delay <= int(time_text[-2:]): # match second
						print('->', tr.td.a.text, ', size:', int(tr.td.span.text[1:-1]), ', second:', int(time_text[-2:]))
						data_list['wiki'].append({'name':tr.td.a.text, 'size':int(tr.td.span.text[1:-1]), 'second':int(time_text[-2:])})

		print()

	except Exception as ex:
		print(ex)
	
	threading.Timer(delay, crawl, [delay]).start()


class GetData(Resource):
	def get(self):
		send_list = {'wiki': []}  # 전송 데이터를 담는다.
		now = datetime.now(pytz.timezone('UTC'))

		for wiki in data_list['wiki']:
			if( wiki['second']==int(now.strftime('%S'))-int(DELAY) ): # 현재 시간에 해당하는 데이터를 전송 데이터에 담는다.
				send_list['wiki'].append({'name':wiki['name'], 'size':wiki['size']})

		# print('send_list:', send_list)
		return send_list,  201, {'Access-Control-Allow-Origin': '*'}


if __name__ == '__main__':
	crawl(DELAY)
	
	api.add_resource(GetData, '/data')
	app.run(host='0.0.0.0')

