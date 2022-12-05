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
    def dateFromSQL(self,dataset):
        connstr='../dataBase/latestDate/latest'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)     
        df=pd.read_sql('select * from latest'+dataset,conn)  
        return df.pivot_table(columns=['date']).columns
    def allDate(self,dataset):
        connstr='../dataBase/latestDate/latest'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)            
        today=datetime.date.today()
        init_date="1994-10-01"
        stock1=self.singleStock('1101',init_date,today,dataset)
        stock2=self.singleStock('2330',init_date,today,dataset)
        if len(stock1)>0 and len(stock2)>0:
            allDataList=pd.concat([stock1,stock2])
            allDataList.to_sql('latest'+dataset,conn,if_exists='replace')
        # return allDataList.pivot_table(columns=['date']).columns
        return self.dateFromSQL(dataset)
    def multiData(self,start_date,dataset):
        connstr='../dataBase/'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)
        multiData=self.multiStock(start_date,dataset)
        if len(multiData)>0:
            multiData.to_sql(dataset+start_date.replace('-','s'),conn,if_exists='replace')
            print(dataset,start_date)
        else:
            print(dataset,start_date+": not exist")
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
                    # latestDate=self.allDate(dataset)[-1]
                    latestDate=self.dateFromSQL(dataset)[-1]
                    column=self.df(latestDate,dataset).pivot_table(columns='type').columns
                    column2=self.df(latestDate,dataset).pivot_table(columns=['type','origin_name']).columns
                    self.allVar[dataset]=column
                    self.typeIndex.extend(column2)
    def checkDB(self,val):
        self.getVar()
        for dataType in self.allVar:
            if val in self.allVar[dataType]:
                return dataType
    def typeDataFromSQL(self,dataset):
        dateList=self.dateFromSQL(dataset)
        tableData=self.tableInSQL(dataset)
        tempDf=pd.DataFrame([])
        for date in dateList:
            tableName=dataset+date.replace('-','s')
            if tableName in tableData:
                df=self.df(date,dataset)
                tempDf=pd.concat([tempDf,df],join='outer')
        return tempDf
    def valData(self,val):
        dataType=self.checkDB(val)
        typeData=self.typeDataFromSQL(dataType)
        valData=typeData[typeData['type'].str.contains(val)]
        return valData
