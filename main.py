from flask import Flask, redirect, url_for, render_template, session, request
from data import *


app = Flask(__name__)

firstNav='overview'
singleDataNav = ['overview', 'month revenue',
                 'income statement']


@app.route("/")
def home():
    return render_template("index.html", firstNav=firstNav,navData=singleDataNav)
# @app.route("/revene/<stockId>")


@app.route("/test/<stockId>")
def test(stockId):
    apiData = FromAPI()
    return apiData.singleStock(stockId, '2022-12-01', '2022-12-10', "TaiwanStockPrice").to_json()


if __name__ == "__main__":
    app.run(debug=True)
