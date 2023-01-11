from flask import Flask, redirect, url_for, render_template, session, request
from data import *
from apiData import *


app = Flask(__name__)
apiData = FromAPI()

firstNav='overview'
singleDataNav = ['overview', 'month revenue',
                 'income statement']


@app.route("/",methods = ['POST', 'GET'])
def home():
    return render_template("index.html", firstNav=firstNav,navData=singleDataNav)
@app.route("/table/<stockId>")
def table(stockId):
    api=API(stockId)
    # allTable={'priceTable':api.priceApi.to_json(),'revenueTable':api.revenueApi.to_json()}
    allTable={'revenueTable':api.revenueApi.to_json()}
    return allTable['revenueTable']


@app.route("/test/<stockId>")
def test(stockId):
    
    return apiData.singleStock(stockId, '2022-12-01', '2022-12-10', "TaiwanStockPrice").to_json()


if __name__ == "__main__":
    app.run(debug=True)
