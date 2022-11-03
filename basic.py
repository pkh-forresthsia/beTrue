import requests
import pandas as pd
from dateManage import *

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