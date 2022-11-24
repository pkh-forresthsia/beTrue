import requests
import pandas as pd
import numpy as np
from dateManage import *
import statistics as stat

class Param():
    def __init__(self):
        self.url="https://api.finmindtrade.com/api/v4/data"
        self.parameter={
            'dataset':'',
            'token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMi0xMC0wNyAxNToxNjowMiIsInVzZXJfaWQiOiJ1dXV1MTExMiIsImlwIjoiNjAuMjQ5LjE4MC4yMDAifQ.U_dDO8vrdB0ieB2hfh7gRz4fc2Z48kIl421UtHqankM'
        }
    def getData(self,parameter):
        resp=requests.get(self.url,params=parameter)
        data=resp.json()
        data=pd.DataFrame(data['data'])
        return data
class BasicFunction():
    def tryEmptyMean(self,arrayData):
        if len(arrayData)==0:
            return 0
        else:
            return stat.mean(arrayData)
    def tryEmptyMax(self,arrayData):
        if len(arrayData)==0:
            return 0
        else:
            return max(arrayData)
    def emptyBool(self,thisSeries,booling):
        try:
            return thisSeries[booling]
        except:
            return 0
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
