from data import *

class MonthData(FromSQL):
    def __init__(self):
        super().__init__()
        self.revenue=self.datasetFromSQL("TaiwanStockMonthRevenue").pivot_table(index='date',columns='stock_id',values='revenue') 
    def revenueData(self):
        revenue=self.revenue
        indexList=list(revenue.index)
        indexMap=dict(zip(list(revenue.index),self.dm.monthTrans(indexList)))
        return revenue.rename(mapper=indexMap,axis=0)
    def nMonthYearIncrease(self,n):
        revenueData=self.revenueData()
        return self.dt.nPeriodIncrease(12,revenueData,n)
        
