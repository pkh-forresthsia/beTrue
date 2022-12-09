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
        return dateList
    def latestDate(self,dataset):
        connstr='../data/latest/'+dataset+".sqlite3"
        conn=sqlite3.connect(connstr)
        dm=DateManage()
        today=dm.todayDate()
        init_date=self.init_date
        self.singleStockToSQL('2330',init_date,today,dataset,ifExist='replace',connstr='../data/latest/')
        self.singleStockToSQL('1101',init_date,today,dataset,ifExist='replace',connstr='../data/latest/')
        latestDate=pd.read_sql("""select distinct date from '%s'"""%(dataset),conn)
        return latestDate
    def downloadBasicPriceData(self):
        latestRevenueDate=self.latestDate("TaiwanStockMonthRevenue").iloc[-1]
        idList=self.multiStock(latestRevenueDate,"TaiwanStockMonthRevenue")['stock_id']
        initDate=self.init_date
        dm=DateManage()
        today=dm.todayDate()
        for stock_id in idList:
            self.singleStockToSQL(stock_id,initDate,today,"TaiwanStockPrice")
    def downloadTypeData(self,dataset):
        latestDate=self.latestDate(dataset)
        for date in latestDate:
            self.multiStockToSQL(date,dataset)
    def updateTypeData(self,dataset):
        latestDate=self.latestDate(dataset)
        dateInSQL=self.dateInSQL(dataset)
        for date in latestDate:
            if date not in dateInSQL:
                self.multiStockToSQL(date,dataset)


# class FromSQL(ToSQL):