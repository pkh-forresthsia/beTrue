from basic import *
import sqlite3
import sys

sys.path.insert(0,'../dataBase')

class FromAPI(Param):
    def __init__(self):
        super().__init__()
    def multiStock(self,start_date,dataset):
        self.parameter['start_date']=start_date
        self.parameter['dataset']=dataset
        return self.getData(self.parameter)
    def singleStock(self,data_id,start_date,end_date,dataset):
        self.parameter['data_id']=data_id
        self.parameter['start_date']=start_date
        self.parameter['end_date']=end_date
        self.parameter['dataset']=dataset
        return self.getData(self.parameter)
    
class DownloadData(FromAPI):
    def __init__(self):
        super().__init__()
    def multiData(self,start_date,dataset):
        connstr='../dataBase/'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)
        multiData=self.multiStock(start_date,dataset)
        multiData.to_sql(dataset+start_date.replace('-','s'),conn)
