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
class StatementManage(Info):
    def __init__(self,start_date,n):
        super().__init__()
        self.start_date=start_date
        self.n=n
        self.nYearDataFromSql=super().nYearDataFromSql(self.start_date,self.n)
    def getType(self,type):
        tempDf=self.nYearDataFromSql
        typeDf=tempDf[tempDf['type']==type]
        return typeDf.pivot_table(values='value',index='date',columns='stock_id')
    def stockRolling(self,typeData,stock_id):
        return typeData[stock_id].rolling(4).sum()
    def rollingIncrease(self,rollingData):
        increase=(rollingData/rollingData.shift()-1)*100
        summaryData=pd.DataFrame({'increase':increase[increase.notnull()],'index':0})
        for i in range(len(summaryData)):
            summaryData['index'].iloc[i]=summaryData['increase'].iloc[i]>0
        return summaryData
    def increasePeriodData(self,increaseData):
        tempPeriod=1
        summaryData=increaseData
        periodSummary={'increasePeriod':[],'decreasePeriod':[],'endPeriod':0}
        for i in range(1,len(summaryData)):
            if summaryData['index'][i]==summaryData['index'][i-1]:
                tempPeriod=tempPeriod+1
            else:
                if summaryData['index'][i]==True:
                    periodSummary["decreasePeriod"].append(tempPeriod)
                else:
                    periodSummary["increasePeriod"].append(tempPeriod)
                tempPeriod=1
        if(len(summaryData)>0):
            if summaryData['index'][-1]==True:
                periodSummary['increasePeriod'].append(tempPeriod)
                periodSummary['endPeriod']=tempPeriod
            else:
                periodSummary['decreasePeriod'].append(tempPeriod)
                periodSummary['endPeriod']=tempPeriod*(-1)
        return periodSummary
    def periodAnalysis(self,type):
        bf=BasicFunction()
        tempData=[]
        typeData=self.getType(type)
        ids=self.nYearDataFromSql.pivot_table(columns='stock_id').columns
        for i in range(len(ids)):
            stockId=ids[i]
            if len(stockId)==4:
                rollingData=self.stockRolling(typeData,stockId)
                rollingIncreaseData=self.rollingIncrease(rollingData)
                increaseNum=rollingIncreaseData.groupby(by=['index'])['increase'].count()
                increaseMeanAll=rollingIncreaseData.groupby(by=['index'])['increase'].mean()
                if(len(rollingIncreaseData))>0 :
                    increasePeriod=self.increasePeriodData(rollingIncreaseData)
                    increasePeriodMean=bf.tryEmptyMean(increasePeriod['increasePeriod'])
                    decreasePeriodMean=bf.tryEmptyMean(increasePeriod['decreasePeriod'])
                    increasePeriodMax=bf.tryEmptyMax(increasePeriod['increasePeriod'])
                    decreasePeriodMax=bf.tryEmptyMax(increasePeriod['decreasePeriod'])
                    increaseProbability=bf.emptyBool(increaseNum,True) /len(rollingIncreaseData)
                    increaseMean=bf.emptyBool(increaseMeanAll,True)
                    decreaseMean=bf.emptyBool(increaseMeanAll,False)
                    expectGrowth=increaseProbability*increaseMean+(1-increaseProbability)*decreaseMean
                    endPeriod=increasePeriod['endPeriod']
                    tempData.append(
                        {'stock_id':stockId,
                        'incPeriodMean':round(increasePeriodMean,1),
                        'decPeriodMean':round(decreasePeriodMean,1),
                        'incPeriodMax':increasePeriodMax,
                        'decPeriodMax':decreasePeriodMax,
                        'endPeriod':endPeriod,
                        'incP':round(increaseProbability,2),
                        'incM':round(increaseMean,1),
                        'decM':round(decreaseMean,1),
                        'growth':round(expectGrowth,1)
                        })
        return pd.DataFrame(tempData) 
        






