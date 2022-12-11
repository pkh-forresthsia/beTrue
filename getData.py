from basic import *
import sqlite3

class FromAPI(Param):
    def __init__(self):
        super().__init__()
    def multiStock(self,start_date,dataset):
        self.parameter['start_date']=start_date
        self.parameter['dataset']=dataset
        return self.getData(self.parameter)
    def singleStock(self,data_id,start_date,end_date,dataset):
        self.parameter2['data_id']=data_id
        self.parameter2['start_date']=start_date
        self.parameter2['end_date']=end_date
        self.parameter2['dataset']=dataset
        print("get data",data_id)
        return self.getData(self.parameter2)

class ToSQL(FromAPI):
    def __init__(self):
        super().__init__()
        self.connstr='../data/'
    def singleStockToSQL(self,data_id,start_date,end_date,dataset,ifExist='append',connstr='../data/'):
        singleStockData=self.singleStock(data_id,start_date,end_date,dataset)
        connstr=connstr+dataset+".sqlite3"
        conn=sqlite3.connect(connstr)
        if len(singleStockData)>0:
            singleStockData.to_sql(dataset,conn,if_exists=ifExist,index=False)
            print(dataset,data_id,start_date,end_date," to sql")
    def multiStockToSQL(self, start_date, dataset,ifExist='append',connstr='../data/'):
        multiStockData=self.multiStock(start_date,dataset)
        connstr=connstr+dataset+".sqlite3"
        conn=sqlite3.connect(connstr)
        if len(multiStockData)>0:
            multiStockData.to_sql(dataset,conn,if_exists=ifExist,index=False)
            print(dataset,start_date," to sql")
    def dateInSQL(self,dataset):
        connstr=self.connstr+dataset+".sqlite3"
        conn=sqlite3.connect(connstr)
        dateList=pd.read_sql("""select distinct date from '%s'"""%(dataset),conn)
        print('date in sql')
        return dateList
    def latestDate(self,dataset):
        connstr='../data/latest/'+dataset+".sqlite3"
        conn=sqlite3.connect(connstr)
        dm=DateManage()
        today=dm.todayDate()
        init_date=self.init_date
        stock1=self.singleStock('1101',init_date,today,dataset)
        print('get stock1')
        stock2=self.singleStock('2330',init_date,today,dataset)
        print('get stock1')
        if len(stock1)>0 and len(stock2)>0:
            allDataList=pd.concat([stock1,stock2])
        allDataList.to_sql(dataset,conn,if_exists='replace')
        latestDate=pd.read_sql("""select distinct date from '%s'"""%(dataset),conn)
        print("read latest date")
        return latestDate
    def downloadBasicPriceData(self,end_date='2022-12-09'):
        latestRevenueDate=self.latestDate("TaiwanStockMonthRevenue").iloc[-1]
        idList=self.multiStock(latestRevenueDate,"TaiwanStockMonthRevenue")['stock_id']
        initDate=self.init_date
        for stock_id in idList:
            self.singleStockToSQL(stock_id,initDate,end_date,"TaiwanStockPrice")
        print('download basic price data')
    def downloadTypeData(self,dataset):
        latestDate=self.latestDate(dataset)
        for date in latestDate:
            self.multiStockToSQL(date,dataset)
        print('download type data')
    def downloadAll(self):
        dm=DateManage()
        today=dm.todayDate()
        self.downloadBasicPriceData(today)
        allType=self.allType
        for type in allType['seasonData']:
            self.downloadTypeData(type)
        print('down load season data')
        for type in allType['monthData']:
            self.downloadTypeData(type)
        print('down load month data')
    def updateTypeData(self,dataset):
        latestDate=self.latestDate(dataset)
        dateInSQL=self.dateInSQL(dataset)
        for i in range(len(latestDate)):
            if latestDate[i] not in dateInSQL:
                self.multiStockToSQL(latestDate[i],dataset)
    def updateAll(self):
        allType=self.allType
        for periodType in allType:
            for type in allType[periodType]:
                self.updateTypeData(type)
                print(type)

class FromSQL(ToSQL):
    def __init__(self):
        super().__init__()
        self.connstr='../data/'
    def singleDataTypeFromSQL(self,stock_id,type,dataset):
        connstr=self.connstr+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)
        if dataset in self.allType['dayData']:
            singleData=pd.read_sql("""select date,stock_id,%s from '%s' where stock_id='%s' order by date"""%(type,dataset,stock_id),conn)
        elif dataset in self.allType['monthData']:
            singleData=pd.read_sql("""select date,stock_id,revenue from '%s' where sotck_id='%s' order by date"""%(dataset,stock_id))
        else:
            singleData=pd.read_sql("""select date,stock_id,value from '%s' where stock_id='%s' and type='%s' order by date"""%(dataset,stock_id,type),conn)
        return singleData
    def singleDataFromSQL(self,stock_id,dataset):
        connstr=self.connstr+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)
        if dataset in self.allType['dayData']:
            singleData=pd.read_sql("""select * from '%s' where stock_id='%s' order by date"""%(dataset,stock_id),conn)
        elif dataset in self.allType['monthData']:
            singleData=pd.read_sql("""select date,stock_id,revenue from '%s' where sotck_id='%s' order by date"""%(dataset,stock_id))
        else:
            singleData=pd.read_sql("""select * from '%s' where stock_id='%s' order by date"""%(dataset,stock_id),conn)
        return singleData        
    def allDataDistinctTypeFromSQL(self,dataset):
        connstr=self.connstr+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)
        if dataset in self.allType['seasonData']:
            distinctType=pd.read_sql("""select distinct type,origin_name from '%s' order by type"""%(dataset),conn)        
        return distinctType