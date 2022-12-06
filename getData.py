from basic import *
from dateManage import *
import sqlite3
import sys

sys.path.insert(0,'../dataBase')

class FromAPI(Param):
    def __init__(self):
        super().__init__()
    # 特定日期的所有股票
    def multiStock(self,start_date,dataset):
        self.parameter['start_date']=start_date
        self.parameter['dataset']=dataset
        return self.getData(self.parameter)
    # 特定區間的特定股票
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
        self.singleStockData={
            'dayData':["TaiwanStockPrice"],
        }
        self.nonFixedPeriodData={
            'dividend':["TaiwanStockDividend"]
        }
class DownloadData(FromAPI):
    def __init__(self):
        super().__init__()
        self.dataType=DataType()
    # 讀取目前資料庫裡最新的日期資料
    def dateFromSQL(self,dataset):
        connstr='../dataBase/latestDate/latest'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)     
        df=pd.read_sql('select * from latest'+dataset,conn)  
        return df.pivot_table(columns=['date']).columns
    # 讀取目前資料庫裡最新的sotck_id資料
    def idListFromSQL(self):
        connstr='../dataBase/latestDate/allId.sqlite3'
        conn=sqlite3.connect(connstr)  
        df=pd.read_sql('select * from latestrevenue',conn)
        return df['stock_id']
    # 更新資料庫日期到最新 並讀取資料庫資料
    def allDate(self,dataset):
        connstr='../dataBase/latestDate/latest'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)            
        today=datetime.date.today()
        if dataset=="TaiwanStockPrice":
            init_date="2022-12-02"
        else:
            init_date="1994-10-01"
        stock1=self.singleStock('1101',init_date,today,dataset)
        stock2=self.singleStock('2330',init_date,today,dataset)
        if len(stock1)>0 and len(stock2)>0:
            allDataList=pd.concat([stock1,stock2])
            allDataList.to_sql('latest'+dataset,conn,if_exists='replace')
        return self.dateFromSQL(dataset)
    # 更新資料庫月營收日期到最新 拿到最新日期的月營收資料 並從月營收資料拿到stock_id
    def allId(self):
        connstr='../dataBase/latestDate/allId.sqlite3'
        conn=sqlite3.connect(connstr)           
        latestDate=self.allDate('TaiwanStockMonthRevenue')[-1]
        latestRevenue=self.multiStock(latestDate,'TaiwanStockMonthRevenue')
        latestRevenue.to_sql('latestRevenue',conn,if_exists='replace')
        # return latestRevenue['stock_id']
        return self.idListFromSQL()
    # 從所有各別公司下載特定區間的股票資料
    def downloadSingleStockPrice(self,dataset="TaiwanStockPrice"):
        idData=self.allId()
        start_date='1990-01-01'
        end_date='2022-12-01'
        singlelDataset='single'+dataset
        tableData=self.tableInSQL(singlelDataset)
        for data_id in idData:
            tableName=dataset+data_id
            if tableName not in tableData:
                self.singleData(data_id,start_date,end_date,dataset)
    #下載特定日期的特定類別所有資料
    def multiData(self,start_date,dataset):
        connstr='../dataBase/'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)
        multiData=self.multiStock(start_date,dataset)
        if len(multiData)>0:
            multiData.to_sql(dataset+start_date.replace('-','s'),conn,if_exists='replace')
            print(dataset,start_date)
        else:
            print(dataset,start_date+": not exist")
    def singleData(self,data_id,start_date,end_date,dataset):
        connstr='../dataBase/single'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)
        singleData=self.singleStock(data_id,start_date,end_date,dataset)
        if len(singleData)>0:
            singleData.to_sql(dataset+data_id,conn,if_exists='replace')
            print(dataset,data_id)
        else:
            print(dataset,data_id+": not exist")

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
        self.downloadSingleStockPrice()
class Read(DownloadData):
    def __init__(self):
        super().__init__()
        self.allVar={
            'TaiwanStockMonthRevenue':['revenue']
        }
        self.typeIndex=[]
    # 以日期還有特定類別決定的資料
    def df(self,start_date,dataset):
        connstr='../dataBase/'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)
        df=pd.read_sql('select * from '+dataset+start_date.replace('-','s'),conn)
        return df
    # 以公司代號還有特定類為主的資料
    def singleDf(self,data_id,dataset):
        connstr='../dataBase/single'+dataset+'.sqlite3'
        conn=sqlite3.connect(connstr)
        df=pd.read_sql('select * from '+dataset+data_id,conn)
        return df
    # 拿到所有的變數代號和變數
    def getVar(self):
        fixedPeriodData=self.dataType.fixedPeriodData
        for periodType in fixedPeriodData:
            for dataset in fixedPeriodData[periodType]:
                latestDate=self.dateFromSQL(dataset)[-1]
                if periodType=='seasonData':
                    column=self.df(latestDate,dataset).pivot_table(columns='type').columns
                    column2=self.df(latestDate,dataset).pivot_table(columns=['type','origin_name']).columns
                    self.allVar[dataset]=column
                    self.typeIndex.extend(column2)
                if periodType=='dayData':
                    dfT=self.df(latestDate,dataset).set_index(keys=["date","stock_id","index"])
                    column=dfT.columns
                    self.allVar[dataset]=column
    # 找變數源頭的類別
    def checkDB(self,val):
        self.getVar()
        for dataType in self.allVar:
            if val in self.allVar[dataType]:
                return dataType
    def singleStockTypeDataFromSQL(self,dataset):
        idList=self.idListFromSQL()
        tempDf=pd.DataFrame([])
        for data_id in idList:
            singleDf=self.singleDf(data_id,dataset)
            tempDf=pd.concat([tempDf,singleDf],join='outer')
            print("concat data_id",data_id)
        return tempDf
    def typeDataFromSQL(self,dataset):
        dateList=self.dateFromSQL(dataset)
        tableData=self.tableInSQL(dataset)
        tempDf=pd.DataFrame([])
        for date in dateList:
            tableName=dataset+date.replace('-','s')
            if tableName in tableData:
                df=self.df(date,dataset)
                tempDf=pd.concat([tempDf,df],join='outer')
        if dataset=="TaiwanStockPrice":
            initData=self.singleStockTypeDataFromSQL(dataset)
            tempDf=pd.concat([initData,tempDf],join='outer')
        return tempDf
    def valData(self,val):
        dataType=self.checkDB(val)
        typeData=self.typeDataFromSQL(dataType)
        if dataType =='TaiwanStockMonthRevenue':
            valData=typeData.pivot_table(values='revenue',index='date',columns='stock_id')
            return valData
        elif dataType=='TaiwanStockPrice':
            valData=type.pivot_table(values=val,index='date',columns='stock_id')
            return valData
        else:
            valData=typeData[typeData['type'].str.contains(val)]
            return valData.pivot_table(values='value',index='date',columns='stock_id')
class Combine(Read):
    def __init__(self):
        super().__init__()
        self.connstr='../dataBase/combineData/'
    def initCombine(self):
        fixPeriodData=self.dataType.fixedPeriodData
        for period in fixPeriodData:
            for type in fixPeriodData[period]:
                typeData=self.typeDataFromSQL(type)
                connstr=self.connstr+type+'.sqlite3'
                conn=sqlite3.connect(connstr)
                typeData.to_sql(type,conn,if_exists='replace')
                print(type)
    def updateCombine(self):
        fixPeriodData=self.dataType.fixedPeriodData
        for period in fixPeriodData:
            for type in fixPeriodData[period]:
                combineData=self.read(type) 
                combineDateList=combineData.pivot_table(columns="date").columns
                tableData=self.tableInSQL(type) 
                for tableName in tableData:
                    if tableName.replace(type,"").replace("s","-") not in combineDateList:
                              
        return
    def read(self,type):
            connstr=self.connstr+type+'.sqlite3'
            conn=sqlite3.connect(connstr)
            typeData=pd.read_sql('select * from '+type,conn)
            return typeData        
