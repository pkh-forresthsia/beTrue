from price import *
from statement import *

class StatementModel(StatementManage):
    def __init__(self,start_date,n):
        super().__init__(start_date,n)
        self.start_date=start_date
        self.n=n
        dayInfo=DayInfoAll()
        self.thisPrice=dayInfo.getAllPriceData(start_date)
    def latestAnalysis(self,type="IncomeAfterTax"):
        tempData=[]
        thisPrice= self.thisPrice[['stock_id','close']]
        typeData=self.getType(type)
        typeData2=self.getType("TotalNonbusinessIncome")
        typeData=typeData-typeData2        
        epsData=self.getType("EPS")
        ids=typeData.columns
        for item in ids:
            stockId=item
            if len(stockId)==4:
                rollingData=self.stockRolling(typeData,stockId)
                epsRolling=self.stockRolling(epsData,stockId)
                rollingIncreaseData=self.rollingIncrease(rollingData,4)
                if len(rollingIncreaseData)>0:
                    season4Inc=rollingIncreaseData['increase'].iloc[-1]
                    seasonInc=self.rollingIncrease(rollingData,1)['increase'].iloc[-1]
                    eps=epsRolling.iloc[-1]
                    growthRate=[seasonInc,season4Inc]
                    maxEps=max(eps,0)
                    maxGrowthRate=max(min(max(growthRate),20),-20)/100
                    minGrowthRate=min(max(min(growthRate),-20),20)/100
                    overRate=min(100*eps,self.estimatePrice(maxEps,maxGrowthRate))
                    underRate=min(100*eps,self.estimatePrice(maxEps,minGrowthRate))
                    tempData.append({
                        'stock_id':stockId,
                        'EPS':round(eps,2),
                        '季成長':round(seasonInc),
                        '年成長':round(season4Inc),
                        '樂觀估計':max(round(overRate),0),
                        '悲觀估計':max(round(underRate),0)
                    })
        thisData=pd.DataFrame(tempData)
        tempData=pd.merge(thisPrice,thisData,how='inner')
        tempData['估價差距%']=round((tempData['悲觀估計']/tempData['close']-1)*100)
        return tempData[tempData['close']!=0]
    def estimateDiscoount(self,tempData):
        tempData['成長估計%']=0
        for i in range(len(tempData)):
            if tempData['close'].iloc[i]>0 and tempData['EPS'].iloc[i]>0 and tempData['估價差距%'].iloc[i]>10:
                tempData['成長估計%'].iloc[i]=round(100*self.discountRate(tempData['EPS'].iloc[i],tempData['close'].iloc[i]))
                print(tempData.iloc[i])
        return tempData
