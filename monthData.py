from data import *

class MonthData(FromSQL):
    def __init__(self):
        super().__init__()
        self.revenue=self.datasetFromSQL("TaiwanStockMonthRevenue")  
    def revenueData(self):
        revenueData=self.revenue
        revenueData['date']=revenueData['revenue_year']+"-"+revenueData['revenue_month']+"-10"
        return revenueData