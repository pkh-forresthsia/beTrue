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
        ids=typeData.columns
        for item in ids:
            stockId=item
            if len(stockId)==4:
                rollingData=self.stockRolling(typeData,stockId)
                rollingIncreaseData=self.rollingIncrease(rollingData)
                if len(rollingIncreaseData)>0:
                    season4Inc=rollingIncreaseData.iloc[-1]
                    seasonInc=self.rollingIncrease(rollingData,1)['increase'].iloc[-1]
                    tempData.append({
                        'stock_id':stockId,
                        '季成長':round(seasonInc),
                        '年成長':round(season4Inc)
                    })
        thisData=pd.DataFrame(tempData)
        # tempData=pd.merge(thisPrice,tempData,how='inner')
        return thisData
