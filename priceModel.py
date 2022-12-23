from dayData import *
from seasonData import *

class DiscountModel(StatementData):
    def __init__(self):
        super().__init__()   
        self.infoId=InfoId()
        # self.latestDay=self.latestDate("TaiwanStockPrice").iloc[-1]
    def discountRate(self,eps,price,g=0.02,e=0.1):
        if eps<0:
            return -100
        else:
            tempPrice=0
            r=(1+g)/(1+e)
            x=symbols('x')
            S=solve(eps*x*(1-x**5)+eps*x**5*(1-x)*r/(1-r)-price*(1-x))
            for i in range(len(S)):
                if S[i]!=1 and S[i]>0:
                    tempPrice=S[i]*(1+e)-1
                    return tempPrice
    def latestPrice(self):
        return self.latestDataFromSQL("TaiwanStockPrice").set_index('stock_id')['close']
    def priceEstimateDifferTable(self,priceEstimateTable):
        latestPrice=self.latestPrice()
        data=pd.DataFrame({'price':latestPrice})
        data=pd.merge(priceEstimateTable,data,right_index=True,left_index=True)
        data['priceHigher']=round((data['price']/data['estimatePrice']-1)*100)
        data['growth']=round(data['growth']*100,1)
        data=data[data['price']!=0]
        return self.infoId.mergeIdIndex(data)
        # return data
    def defaultPriceEstimateDifferTable(self,n=5):
        priceEstimateTable=self.defaultPriceEstimateTable(n)
        return self.priceEstimateDifferTable(priceEstimateTable)
    def discountTable(self,epsSeries):
        data=pd.DataFrame({'EPS4season':round(epsSeries,2),'price':self.latestPrice()})
        data=data[(data['EPS4season'].notna())&(data['price'].notna())]
        data['disRate']=-100
        data['EPS4season']=round(data['EPS4season'],2)
        data=data[(data['EPS4season']>0)&data['price']>0]
        data['pe']=data['price']/data['EPS4season']
        data['disRate']=data.apply(lambda row:self.peMap(row['pe']),axis=1)
        return data
    def estimateDiffTable(self,priceEstimateTable,discountTable):
        df=pd.merge(priceEstimateTable,discountTable,right_index=True,left_index=True)
        data=df[(df['estimatePrice']!=0)&(df['price']!=0)]
        data['growth']=round(data['growth']*100,1)
        data['pe']=round(data['pe'],1)
        data['priceHigher']=round((data['price']/data['estimatePrice']-1)*100)
        data['growthHigher']=round((data['growth']/data['disRate']-1)*100)
        data=data[['growth','disRate','growthHigher','estimatePrice','price','pe','EPS4season_x','priceHigher']].sort_values(by='priceHigher')
        return  self.infoId.mergeIdIndex(data)