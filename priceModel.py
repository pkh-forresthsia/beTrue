from dayData import *
from seasonData import *

class DiscountModel(StatementData):
    def __init__(self):
        super().__init__()   
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
        data=data[data['price']!=0]
        return data
    def discountTable(self,epsSeries):
        data=pd.DataFrame({'EPS4season':round(epsSeries,2),'price':self.latestPrice()})
        data=data[(data['EPS4season'].notna())&(data['price'].notna())]
        data['disRate']=-100
        print('stock_id,4seasonEPS,price,discountRate')
        for i in range(len(data)):
            if data['EPS4season'][i]>0 and data['price'][i]>0:
                data['disRate'][i]=self.discountRate(round(data['EPS4season'][i],2),data['price'][i])*100
                print(data.index[i],',',data['EPS4season'][i],',',data['price'][i],',',data['disRate'][i])
                # print(data.index[i],data['EPS4season'][i],data['price'][i])
        return data
    def estimateDiffTable(self,priceEstimateTable,discountTable):
        df=pd.merge(priceEstimateTable,discountTable,right_index=True,left_index=True)
        data=df[(df['estimatePrice']!=0)&(df['price']!=0)]
        data['priceHigher']=round((data['price']/data['estimatePrice']-1)*100)
        data['growthHigher']=round((data['growth']/data['disRate']-1)*100)
        data['pd']=round(data['price']/data['EPS4season_x'],1)
        return data[['growth','disRate','estimatePrice','price','EPS4season_x','growthHigher','priceHigher']].sort_values(by='priceHigher')
