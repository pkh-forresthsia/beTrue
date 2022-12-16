from data import *

class MonthData(FromSQL):
    def __init__(self):
        super().__init__()
        self.revenue=self.datasetFromSQL("TaiwanStockMonthRevenue").pivot_table(index='date',columns='stock_id',values='revenue')    
