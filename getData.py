from basic import *
from dateManage import *
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
        self.parameter2['data_id']=data_id
        self.parameter2['start_date']=start_date
        self.parameter2['end_date']=end_date
        self.parameter2['dataset']=dataset
        return self.getData(self.parameter2)
    
class DataType():
    def __init__(self):
        self.fixedPeriodData={
            'seasonData':[
                "TaiwanStockFinancialStatements",
                "TaiwanStockBalanceSheet",
                "TaiwanStockCashFlowsStatement",
            ],
            'monthData':["TaiwanStockMonthRevenue"],
            'dayData':["TaiwanStockPrice"],
        }
        self.nonFixedPeriodData={
            'dividend':["TaiwanStockDividend"]
        }
class DownloadData(FromAPI):
    def __init__(self):
        super().__init__()
        self.dataType=DataType()
    def allDate(self,dataset):
        today=datetime.date.today()
        init_date="1990-01-01"
        stock1=self.singleStock('1101',init_date,today,dataset)
        stock2=self.singleStock('2330',init_date,today,dataset)
        return pd.concat([stock1,stock2]).pivot_table(columns=['date']).columns
    def multiData(self,start_date,dataset):
        connstr='../dataBase/'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)
        multiData=self.multiStock(start_date,dataset)
        if len(multiData)>0:
            multiData.to_sql(dataset+start_date.replace('-','s'),conn,if_exists='replace')
            print(dataset,start_date)
    def tableInSQL(self,dataset):
        connstr='../dataBase/'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)
        cursor=conn.execute("select name from sqlite_master where type='table'")
        tables=[
            v[0] for v in cursor.fetchall()
            if v[0] !="sqlite_sequence"
        ]
        cursor.close()
        return tables
    def downloadTypeData(self,dataset):
        dateList=self.allDate(dataset)
        tableData=self.tableInSQL(dataset)
        for date in dateList:
            tableName=dataset+date.replace('-','s')
            if tableName not in tableData[:-1]:
                self.multiData(date,dataset)        
    def downloadSamePeriod(self,periodType):
        fixedPeriodData=self.dataType.fixedPeriodData
        for type in fixedPeriodData[periodType]:
            self.downloadTypeData(type)
    def updateAll(self):
        fixedPeriodData=self.dataType.fixedPeriodData
        for type in fixedPeriodData:
            self.downloadSamePeriod(type)
class Read(DownloadData):
    def __init__(self):
        super().__init__()
        self.allVar={
            'TaiwanStockMonthRevenue':['revenue']
        }
        self.typeIndex=[]
    def df(self,start_date,dataset):
        connstr='../dataBase/'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)
        df=pd.read_sql('select * from '+dataset+start_date.replace('-','s'),conn)
        return df
    # def dfTrans(self,df,dataset):
    #     fixedPeriodData=self.dataType.fixedPeriodData
    #     if dataset in fixedPeriodData['seasonData']:
    #         dftrans=pd.pivot_table(values)
    #         return fixedPeriodData
    def getVar(self):
        fixedPeriodData=self.dataType.fixedPeriodData
        for periodType in fixedPeriodData:
            if periodType=='seasonData':
                for dataset in fixedPeriodData[periodType]:
                    latestDate=self.allDate(dataset)[-1]
                    column=self.df(latestDate,dataset).pivot_table(columns='type').columns
                    column2=self.df(latestDate,dataset).pivot_table(columns=['type','origin_name']).columns
                    self.allVar[dataset]=column
                    self.typeIndex.extend(column2)
    def checkDB(self,val):
        if len(self.allVar)<=1:
            self.getVar()
        for dataType in self.allVar:
            if val in self.allVar[dataType]:
                return dataType