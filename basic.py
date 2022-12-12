import requests
import pandas as pd
import numpy as np
import copy
from dateManage import *

class Param():
    def __init__(self):
        self.url="https://api.finmindtrade.com/api/v4/data"
        self.parameter={
            'token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMi0xMC0wNyAxNToxNjowMiIsInVzZXJfaWQiOiJ1dXV1MTExMiIsImlwIjoiNjAuMjQ5LjE4MC4yMDAifQ.U_dDO8vrdB0ieB2hfh7gRz4fc2Z48kIl421UtHqankM'
        }
        self.parameter2=copy.copy(self.parameter)  
        self.init_date='1990-01-01'
        self.allType={
            'monthData':["TaiwanStockMonthRevenue"],
            'dayData':["TaiwanStockPrice"],     
            'seasonData':[
                "TaiwanStockFinancialStatements",
                "TaiwanStockBalanceSheet",
                "TaiwanStockCashFlowsStatement",
            ],   
        }
        self.typeInDataset={
            "TaiwanStockMonthRevenue":['revenue'],
            "TaiwanStockPrice":['Trading_Volume','Trading_money','open','max','min','close','spread','Trading_turnover']
        }
    def getData(self,parameter):
        resp=requests.get(self.url,params=parameter)
        try:
            data=resp.json()
            data=pd.DataFrame(data['data'])
            return data
        except:
            print('request error')      