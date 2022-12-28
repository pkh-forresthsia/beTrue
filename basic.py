import requests
import pandas as pd
import numpy as np
import copy
from dateManage import *
import warnings

warnings.filterwarnings('ignore')
# pd.set_option('display.max_columns',None)
# pd.set_option('display.max_rows',None)

class Param():
    def __init__(self):
        self.url="https://api.finmindtrade.com/api/v4/data"
        self.parameter={
            'token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMi0xMC0wNyAxNToxNjowMiIsInVzZXJfaWQiOiJ1dXV1MTExMiIsImlwIjoiNjAuMjQ5LjE4MC4yMDAifQ.U_dDO8vrdB0ieB2hfh7gRz4fc2Z48kIl421UtHqankM'
        }
        self.parameter2=copy.copy(self.parameter)  
        self.init_date='2006-01-01'
        self.allDataset={
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
        self.yearDate=250
        self.monthDate=20
        self.seasonDate=60
        self.yearMonth=12
        self.seasonMonth=3
        
    def getData(self,parameter):
        resp=requests.get(self.url,params=parameter)
        try:
            data=resp.json()
            data=pd.DataFrame(data['data'])
            return data
        except:
            print('request error')    
class InfoId(Param):
    def __init__(self):
        super().__init__()
        self.parameter['dataset']="TaiwanStockInfo"
    def getId(self):
        ids=super().getData(self.parameter)[['stock_id','stock_name','industry_category']]
        return ids[~ids['industry_category'].isin(['電子工業','化學生技醫療'])]
    def mergeId(self,data):
        ids=self.getId()
        return pd.merge(ids,data,how="inner")  
    def mergeIdIndex(self,indexTable):
        ids=self.getId().set_index('stock_id')
        return pd.merge(ids,indexTable, left_index=True, right_index=True)         
class DataTrans():
    def nMean(self,n,pivotTable):
        return pivotTable.rolling(n).mean()
    def nSum(self,n,pivotTable):
        return pivotTable.rolling(n).sum()
    def nShift(self,n,pivotTable):
        return pivotTable.shift(n,axis=0)
    def nPeriodIncrease(self,n,pivotTable,m=1):
        mTable=self.nMean(m,pivotTable)
        return round((mTable/self.nShift(n,mTable)-1)*100)