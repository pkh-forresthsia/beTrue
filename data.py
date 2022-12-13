from basic import *
import sqlite3

class FromAPI(Param):
    def __init__(self):
        super().__init__()
        self.dm=DateManage()
    def multiStock(self,start_date,dataset):
        self.parameter['start_date']=start_date
        self.parameter['dataset']=dataset
        try:
            getData=self.getData(self.parameter)
            print("get multi data: ")
            return getData
        except:
            print("multi data does not get: ",start_date,dataset)
    def singleStock(self,data_id,start_date,end_date,dataset):
        self.parameter2['data_id']=data_id
        self.parameter2['start_date']=start_date
        self.parameter2['end_date']=end_date
        self.parameter2['dataset']=dataset
        try:
            getData=self.getData(self.parameter2)
            print("get single data: ",data_id,start_date,end_date,dataset)
            return getData
        except:
            print("single data does not get: ",data_id,start_date,end_date,dataset)
    def addStamp(self,dataFrame):
        dataFrame['dateStamp']=0
        for i in range(len(dataFrame)):
            dataFrame['dateStamp'][i]=self.dm.getTimeStamp(dataFrame['date'][i]) 
        return dataFrame
class ToSQL(FromAPI):
    def __init__(self):
        super().__init__()
        self.connstr1='../data/'
        self.connstr2='../data/latest/'
    def singleStockToSQL(self,data_id,start_date,end_date,dataset,update=1):
        singleStockData=self.singleStock(data_id,start_date,end_date,dataset)
        singleStockData=self.addStamp(singleStockData)
        if update==1:
            connstr=self.connstr1+dataset+'.db'
            conn=sqlite3.connect(connstr)
            singleStockData.to_sql(dataset,conn,if_exists='append',index=False)
            print("update data",data_id,start_date,end_date,dataset)
        else:
            connstr=self.connstr2+dataset+'.db'
            conn=sqlite3.connect(connstr)
            # print(singleStockData)
            singleStockData.to_sql(dataset,conn,if_exists='replace',index=False)
            print('latest data',data_id,start_date,end_date,dataset)
    def multiStockToSQL(self,start_date,dataset,update=1):
        multiStockData=self.multiStock(start_date,dataset)
        multiStockData=self.addStamp(multiStockData)
        if update==1:
            connstr=self.connstr1+dataset+'.db'
            conn=sqlite3.connect(connstr)
            multiStockData.to_sql(dataset,conn,if_exists='append',index=False)
            print("update data",start_date,dataset)
        else:
            connstr=self.connstr2+"ids"+dataset+'.db'
            conn=sqlite3.connect(connstr)
            multiStockData.to_sql(dataset,conn,if_exists='replace',index=False)
            print('latest data',start_date,dataset)
class Update(ToSQL):
    def __init__(self):
        super().__init__()
        self.dm=DateManage()
    def updateDate(self):
        allDataset=self.allDataset
        init_date=self.init_date
        today=self.dm.todayDate()
        for period in allDataset:
            # print(allDataset[period][0])
            self.singleStockToSQL('1101',init_date,today,allDataset[period][0],0) 
            self.singleStockToSQL('2330',init_date,today,allDataset[period][0],0)
    def latestDate(self,dataset):
        connstr=self.connstr2+dataset+".db"
        conn=sqlite3.connect(connstr)
        dateList=pd.read_sql("""select date from '%s' order by date"""%(dataset),conn)
        return dateList['date']
    def updateId(self):
        dataset=self.allDataset['monthData'][0]
        latestDate=self.latestDate(dataset).iloc[-1]
        self.multiStockToSQL(latestDate,dataset,0)
    def latestId(self):
        dataset=self.allDataset['monthData'][0]
        connstr=self.connstr2+'ids'+dataset+'.db'
        conn=sqlite3.connect(connstr)
        latestId=pd.read_sql("""select distinct stock_id from '%s'"""%(dataset),conn)
        return latestId['stock_id']
    def downloadSinglePriceData(self):
        dataset=self.allDataset['dayData'][0]
        latestId=self.latestId()
        end_date='2022-11-30'
        init_date=self.init_date
        for stock_id in latestId:
            self.singleStockToSQL(stock_id,init_date,end_date,dataset)


        



        

        
