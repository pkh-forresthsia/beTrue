from data import *
from sympy import *

class SeasonData(FromSQL):
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
class StatementData(SeasonData):
    def __init__(self):
        super().__init__()   
        self.statement=self.datasetTable("TaiwanStockFinancialStatements")
    def typeData(self,type):
        statement=self.statement
        typeData=self.statement[statement['type']==type].pivot_table(index='date',values='value',columns='stock_id')   
        return typeData
    def estimatePrice(self,eps,growth1,growth2=0.02,n=5,g=0.02,e=0.1):
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
    def peTable(self,n=5,growth2=0.02,g=0.02,e=0.1):
        growthPe={'growth':[],'pe':[]}
        growthPeTable=pd.DataFrame(growthPe)
        growthBottom=-50
        for i in range(41):
            growth=growthBottom+2.5*i
            pe=round(self.estimatePrice(1,growth/100,growth2,n,g,e),1)
            growthPeTable=growthPeTable.append({'growth':growth,'pe':pe}, ignore_index=True)
        return growthPeTable
    def peMap(self,pe,n=5,growth2=0.02,g=0.02,e=0.1):
        peTable=self.peTable(n,growth2,g,e)
        for i in range(len(peTable)):
            if pe<=peTable['pe'][i]:
                return peTable['growth'][i]

    def priceEstimateTable(self,epsSeries,growthSeries):
        data=pd.DataFrame({'EPS4season':epsSeries,'growth':growthSeries})
        data['estimatePrice']=0
        data=data[(data['EPS4season']>0)&(~data['growth'].isnull())]
        data['estimatePrice']=round(data.apply(lambda row:self.estimatePrice(row['EPS4season'],row['growth']),axis=1),1)
        return data[data['estimatePrice']!=0]
    def defaultPriceEstimateTable(self,n=5):
        epsData=self.typeData("EPS")
        epsSeries=self.latestSum(epsData)
        incomeAfterTax=self.typeData('IncomeAfterTax')-self.typeData('TotalNonbusinessIncome')
        nYearIncrease=self.nYearIncrease(n,incomeAfterTax)
        priceEstimateTable=self.priceEstimateTable(epsSeries,nYearIncrease)
        return priceEstimateTable

