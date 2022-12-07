from getData import *

class DayData(Combine):
    def __init__(self):
        super().__init__()
        self.stockPrice=self.read('TaiwanStockPrice')
    def price(self,value):
        data=self.stockPrice.pivot_table(values=value,index='date',columns='stock_id')
        return data
class LocalValue(DayData):
    def __init__(self,n):
        super().__init__()
        self.n=n
    def localMax(self,stock_id='TAIEX'):
        priceMax=self.price('max')['stock_id']            