from data import *

class DayData(FromSQL):
    def __init__(self):
        super().__init__()
        self.price=self.datasetFromSQL("TaiwanStockPrice")
        # self.max=self.data('max')
        # self.min=self.data('min')
class LocalValue(DayData):
    def __init__(self):
        super().__init__()
    def getLocal(self,n,type='max',stock_id="TAIEX"):
        if type=='max':
            priceData=self.max[stock_id].dropna()
            priceDataRb=priceData.rolling(n).max()
        else:
            priceData=self.min[stock_id].dropna()
            priceDataRb=priceData.rolling(n).min()
        df=pd.concat({'stockPrice':priceData,'rollingBefore':priceDataRb},axis=1)
        return df