from data import *
from dayData import *

class BackTest(DayData):
    def __init__(self):
        super().__init__()
    def fillConditionDate(self,dataset="TaiwanStockFinancialStatements"):
        priceData=self.priceType('close',self.price)
        if dataset in self.allDataset['seasonData']:
            setDate=pd.DataFrame({'date':self.dm.seasonTrans(self.dateInSQL(dataset))}).set_index('date')
        else:
            setData=pd.DataFrame({'date':self.dm.monthTrans(self.dateInSQL(dataset))}).set_index('date')
        df=pd.concat([priceData,setDate],axis=1).sort_values('date')
    