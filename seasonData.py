from data import *
from sympy import *

class SeasenData(FromSQL):
    def __init__(self):
        super().__init__()    
        self.yearSeason=4
        self.transMap={
            "TaiwanStockFinancialStatements":{
                "IncomeAfterTaxes":"IncomeAfterTax",
                "IncomeFromContinuingOperations":"IncomeAfterTax",
                "TotalNonoperatingIncomeAndExpense":"TotalNonbusinessIncome"
            }
        }
        self.dt=DataTrans()
    def datasetTable(self,dataset):
        datasetFromTable=self.datasetFromSQL(dataset)
        datasetFromTable['type'].replace(to_replace=self.transMap[dataset], inplace= True)
        return datasetFromTable
    def nYearIncrease(self,n,table):
        nperiodIncrease=self.dt.nPeriodIncrease(n*self.yearSeason,table,self.yearSeason).iloc[-1]
        data=nperiodIncrease
        # data=nperiodIncrease.iloc[-1]
        data=data[data.notna()]
        for i in range(len(data)):
            data[i]=(data[i]/100+1)**(1/n)-1
        return data
    def latestSum(self,table):
        data=self.dt.nSum(self.yearSeason,table).iloc[-1]
        data=data[data.notna()]
        return data
class StatementData(SeasenData):
    def __init__(self):
        super().__init__()   
        self.statement=self.datasetTable("TaiwanStockFinancialStatements")
    def typeData(self,type):
        statement=self.statement
        typeData=self.statement[statement['type']==type].pivot_table(index='date',values='value',columns='stock_id')   
        return typeData
    def estimatePrice(self,eps,growth1,growth2=0.02,g=0.02,e=0.1,n=5):
        r=(1+g)/(1+e)
        tempSum=0
        for i in range(10):
            if i<n:
                eps=eps*((1+growth1)/(1+e))
                tempSum=tempSum+eps
            else:
                eps=eps*((1+growth2)/(1+e))
                tempSum=tempSum+eps
        eps=eps*r/(1-r)
        tempSum=tempSum+eps
        return tempSum
    def priceEstimateTable(self,epsSeries,growthSeries):
        data=pd.DataFrame({'EPS4season':epsSeries,'growth':growthSeries})
        data['estimatePrice']=0
        for i in range(len(data)):
            if data['EPS4season'][i]>0 and (data['growth'][i]>=0 or data['growth'][i]<0):
                data['estimatePrice'][i]=self.estimatePrice(data['EPS4season'][i],data['growth'][i])
        return data[data['estimatePrice']!=0]

