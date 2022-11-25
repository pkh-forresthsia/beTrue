from basic import *
import sqlite3
import sys

sys.path.insert(0,'../data')

class DayInfo(Param):
    def __init__(self):
        super().__init__()
        self.parameter['dataset']="TaiwanStockPrice"
        self.priceData=sqlite3.connect('priceData')
    def getPriceData(self,start_date,end_date,data_id):
        self.parameter['start_date']=start_date
        self.parameter['end_date']=end_date
        self.parameter['data_id']=data_id
        return super().getData(self.parameter)
class DayInfoAll(DayInfo):
    def __init__(self):
        super().__init__()
        self.allPriceData=sqlite3.connect('allPriceData')
    def getAllPriceData(self,start_date):
        self.parameter['start_date']=start_date
        return super().getData(self.parameter)

        