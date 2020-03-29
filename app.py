from flask import Flask
from flask_restful import Resource, Api
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

app = Flask(__name__)
api = Api(app)

# 여러 클라이언트가 동시에 실행될 경우 크롤링 횟수 많아지므로, app.py에서 새로운 요청 시 직전 크롤링 시간에서 초가 바뀌지 않았을 경우, 현재 크롤링 해놓은 데이터 전송하기
def crawl():
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
				# 데이터 업데이트 후 크롤링 시 1초씩 늦어서 시간 매칭을 못 한다.
				# -> 현재 시간의 1~2초 전 데이터를 가져온다.
				time_text = tr.find_all('td')[2].time.text
				if now.strftime('%Y-%m-%d %H:%M')[8:] == time_text[8:-3]:
					if int(now.strftime('%S'))-2 == int(time_text[-2:]):
						print('->', tr.td.a.text, ',', int(tr.td.span.text[1:-1]))
						data_list['wiki'].append({'name':tr.td.a.text, 'size':int(tr.td.span.text[1:-1])})
		print()
	except Exception as ex:
		print(ex)
	
	return data_list

class GetData(Resource):
	def get(self):
		data_list = crawl()
		print('datalist',data_list)
		#return {'status': 'success'},  201, {'Access-Control-Allow-Origin': '*'}
		return data_list,  201, {'Access-Control-Allow-Origin': '*'}
api.add_resource(GetData, '/data')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
