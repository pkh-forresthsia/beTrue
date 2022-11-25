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
        bf=BasicFunction()
        typeData=self.getType(type)
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
                    overRate=min(100*eps,self.estimatePrice(max(eps,0),(max(growthRate)/100)))
                    underRate=min(100*eps,self.estimatePrice(max(eps,0),(min(growthRate)/100)))
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
        return tempData
