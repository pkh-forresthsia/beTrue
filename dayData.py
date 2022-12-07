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
    def localValue(self,n,type='max',stock_id="TAIEX"):
        priceData=self.price(type)[stock_id].dropna()
        if type=='max':
            priceDataRb=priceData.rolling(n).max()
        else:
            priceDataRb=priceData.rolling(n).min()
        df=pd.concat({'stockPrice':priceData,'rollingBefore':priceDataRb},axis=1)
        df['rollingAfter']=np.NaN
        df['localValue']='local'+type
        df['rollingAfter']=df['rollingBefore'].shift(-n+1,axis=0)
        df['localValue']=df['rollingBefore']==df['rollingAfter']
        return df[df['localValue']==True] 


        