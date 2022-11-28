from basic import *
import sqlite3
import sys
from sympy import *
from price import *

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
                print(nYearPeriod[i][j])
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
        tempDf["type"]=tempDf["type"].str.replace("IncomeAfterTaxes","IncomeAfterTax")
        tempDf["type"]=tempDf["type"].str.replace("IncomeFromContinuingOperations","IncomeAfterTax")
        tempDf["type"]=tempDf["type"].str.replace("TotalNonoperatingIncomeAndExpense","TotalNonbusinessIncome")
        return tempDf.sort_values(['date'],ascending=True)
class StatementManage(Info):
    def __init__(self,start_date,n):
        super().__init__()
        self.start_date=start_date
        self.n=n
        self.nYearDataFromSql=super().nYearDataFromSql(self.start_date,self.n)
    def getType(self,type):
        tempDf=self.nYearDataFromSql
        typeDf=tempDf[tempDf['type'].str.contains(type)]
        return typeDf.pivot_table(values='value',index='date',columns='stock_id')
    def stockRolling(self,typeData,stock_id):
        return typeData[stock_id].rolling(4).sum()
    def rollingIncrease(self,rollingData,n=1):
        increase=(rollingData/rollingData.shift(n)-1)*100
        summaryData=pd.DataFrame({'increase':increase[increase.notnull()],'index':0})
        for i in range(len(summaryData)):
            summaryData['index'].iloc[i]=summaryData['increase'].iloc[i]>0
        return summaryData
    def discountRate(self,eps,price,g=0.02,e=0.1):
        if eps<0:
            return -100
        else:
            tempPrice=0
            r=(1+g)/(1+e)
            x=symbols('x')
            S=solve(eps*x*(1-x**5)+eps*x**5*(1-x)*r/(1-r)-price*(1-x))
            for i in range(len(S)):
                if S[i]!=1 and S[i]>0:
                    tempPrice=S[i]*(1+e)-1
                    return tempPrice
    def estimatePrice(self,eps,growth1,growth2=0.02,g=0.02,e=0.1):
        r=(1+g)/(1+e)
        tempSum=0
        for i in range(10):
            if i<5:
                eps=eps*((1+growth1)/(1+e))
                tempSum=tempSum+eps
            else:
                eps=eps*((1+growth2)/(1+e))
                tempSum=tempSum+eps
        eps=eps*r/(1-r)
        tempSum=tempSum+eps
        return tempSum
    def priceModel(self,type):
        typeData=self.getType(type)
        ids=typeData.columns
        tempData=[]
        for item in ids:
            stockId=item
            if len(stockId)==4:
                rollingData=self.stockRolling(typeData,stockId)
                rollingIncreaseData=self.rollingIncrease(rollingData,4)
                if(len(rollingIncreaseData)>0):
                    increase=rollingIncreaseData.iloc[-1].increase
                    tempData.append({
                        'stock_id':stockId,
                        'increaseYear':round(increase)})

        return pd.DataFrame(tempData)
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
    def periodAnalysis(self,type="IncomeAfterTax"):
        bf=BasicFunction()
        tempData=[]
        typeData=self.getType(type)
        typeData2=self.getType("TotalNonbusinessIncome")
        typeData=typeData-typeData2
        ids=typeData.columns
        for item in ids:
            stockId=item
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
                    dataNum=len(rollingIncreaseData)
                    increaseProbability=bf.emptyBool(increaseNum,True) /dataNum
                    increaseMean=bf.emptyBool(increaseMeanAll,True)
                    decreaseMean=bf.emptyBool(increaseMeanAll,False)
                    expectGrowth=increaseProbability*increaseMean+(1-increaseProbability)*decreaseMean
                    endPeriod=increasePeriod['endPeriod']
                    tempData.append(
                        {'stock_id':stockId,
                        '季數':dataNum,
                        '平均上升季數':round(increasePeriodMean,1),
                        '*下跌1*':round(decreasePeriodMean,1),
                        '最大上升季數':increasePeriodMax,
                        '*下跌2*':decreasePeriodMax,
                        '最新上升季數':endPeriod,
                        'incP':round(increaseProbability,2),
                        'incM':round(increaseMean,1),
                        'decM':round(decreaseMean,1),
                        'growth':round(expectGrowth,1)
                        })
        return pd.DataFrame(tempData) 
    def longPeriodAnalysis(self,periodData):
        dayInfo=DayInfoAll()
        self.thisPrice=dayInfo.getAllPriceData(self.start_date)
        thisPrice= self.thisPrice[['stock_id','close']]
        typeData=periodData[['stock_id','季數','incP','growth']]
        epsData=self.getType("EPS")
        tempData=pd.merge(thisPrice,typeData,how='inner').set_index('stock_id')
        tempData['價格估計']=0
        tempData['eps']=0
        ids=tempData.index
        for item in ids:
            stockId=item
            if len(stockId)==4:
                epsRolling=self.stockRolling(epsData,stockId)
                if len(epsRolling)>0:
                    eps=max(epsRolling.iloc[-1],0)
                    growth=tempData['growth'].loc[stockId]
                    if eps>0:
                        priceEstimate=self.estimatePrice(eps,growth)
                    tempData['eps'].loc[stockId]=round(eps,1)
                    tempData['價格估計'].loc[stockId]=round(priceEstimate,0)
        
        return tempData





