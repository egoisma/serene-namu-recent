from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
	return "<font size=7>Hello</font>"
if __name__=="__main__":
	app.run(host="localhost", port="80")