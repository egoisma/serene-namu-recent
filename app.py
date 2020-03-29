from flask import Flask
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

class GetData(Resource):
    def get(self):
	# crawl here and return
	url = "https://namu.wiki/RecentChanges"
	res = requests.get(url)
	print(response.text)
        return {'status': 'success'},  201, {'Access-Control-Allow-Origin': '*'}

api.add_resource(GetData, '/get')

if __name__ == '__main__':
    app.run(debug=True)
