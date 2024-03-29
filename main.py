from flask import Flask, redirect, url_for, render_template, session, request
from data import *
from apiData import *
import json


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
    allTable={'overviewTable':api.priceApi.to_json(),'revenueTable':api.revenueApi.to_json()}
    return json.dumps(allTable) 

@app.route("/test/<stockId>")
def test(stockId):
    
    return apiData.singleStock(stockId, '2022-12-01', '2022-12-10', "TaiwanStockPrice").to_json()


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
