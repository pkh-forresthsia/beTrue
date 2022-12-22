from data import *

class MonthData(FromSQL):
    def __init__(self):
        super().__init__()
        self.revenue=self.datasetFromSQL("TaiwanStockMonthRevenue").pivot_table(index='date',columns='stock_id',values='revenue') 
        self.yearMonth=12
        self.seasonMonth=3
    def revenueData(self):
        revenue=self.revenue
        indexList=list(revenue.index)
        indexMap=dict(zip(list(revenue.index),self.dm.monthTrans(indexList)))
        return revenue.rename(mapper=indexMap,axis=0)