from basic import *
import sqlite3
import sys

sys.path.insert(0,'../data')

class Info(Param):
    def __init__(self):
        super().__init__()
        self.parameter['dataset']="TaiwanStockFinancialStatements"
        self.statement=sqlite3.connect('statementData.sqlite3')
    def getAll(self,start_date):
        self.parameter['start_date']=start_date
        return super().getData(self.parameter)
    def nYearStatement(self,start_date,n):
        sd=SeasonData(start_date)
        nYearPeriod=sd.nYearPeriod(n)
        for i in range(n):
            for j in range(4):
                thisStatement=self.getAll(nYearPeriod[i][j])
                thisStatement.to_sql('statement'+nYearPeriod[i][j].replace('-','s'),self.statement,if_exists='replace')
    def nYearDataFromSql(self,start_date,n):
        sd=SeasonData(start_date)
        nYearPeriod=sd.nYearPeriod(n)
        tempDf=pd.DataFrame([])
        conn=sqlite3.connect('../data/statementData.sqlite3')
        for i in range(len(nYearPeriod)):
            for j in range(4):
                thisSeason=nYearPeriod[i][3-j]
                df=pd.read_sql('select * from statement'+thisSeason.replace('-','s'),conn)
                tempDf=pd.concat([tempDf,df],join='outer')
        return tempDf.sort_values(['date'],ascending=True)
    def getType(self,start_date,n,type):
        tempDf=self.nYearDataFromSql(start_date,n)
        typeDf=tempDf[tempDf['type']==type]
        return typeDf.pivot_table(values='value',index='date',columns='stock_id')

