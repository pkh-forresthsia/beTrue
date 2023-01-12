from data import *

class API(FromAPI):
    def __init__(self,stock_id):
        super().__init__()    
        self.start_date="2001-01-01"
        self.today=self.dm.transToString(self.dm.todayDate())
        self.stock_id=stock_id
        self.revenueApi=self.revenueApi()
        self.priceApi=self.priceApi()
        # self.financialApi=self.financialApi()
    def revenueApi(self):
        return self.singleStock(self.stock_id,self.start_date,self.today,"TaiwanStockMonthRevenue")
    def priceApi(self):
        return self.singleStock(self.stock_id,self.start_date,self.today,"TaiwanStockPrice")
    def financialApi(self):
        return self.singleStock(self.stock_id,self.start_date,self.today,"TaiwanStockFinancialStatements")
    def revenueTable(self,revenueDataFrame):
        return

