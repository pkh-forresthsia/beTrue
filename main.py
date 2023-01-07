from flask import Flask, redirect, url_for, render_template, session, request
from data import *


app = Flask(__name__)

singleDataNav = ['overview', 'month revenue',
                 'income statement', 'evaluate price']


@app.route("/")
def home():
    return render_template("index.html", navData=singleDataNav)


@app.route("/test")
def test():
    apiData = FromAPI()
    return apiData.singleStock('2330', '2022-12-01', '2022-12-10', "TaiwanStockPrice").to_json()


if __name__ == "__main__":
    app.run(debug=True)
