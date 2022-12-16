from data import *

class DayData(FromSQL):
    def __init__(self):
        super().__init__()
        self.price=self.datasetFromSQL("TaiwanStockPrice")
        self.connstrLocalValue='../data/localValue/'
class LocalValue(DayData):
    def __init__(self):
        super().__init__()
    def getLocal(self,n,type='max',stock_id="TAIEX"):
        priceData=self.price.pivot_table(index='date',values=type,columns='stock_id')[stock_id]
        if type=='max':
            # priceData=self.max[stock_id].dropna()
            priceDataRb=priceData.rolling(n).max()
        else:
            priceDataRb=priceData.rolling(n).min()
        df=pd.concat({'stockPrice':priceData,'rollingBefore':priceDataRb},axis=1)
        df['rollingAfter']=df['rollingBefore'].shift(-n+1,axis=0)
        df['localcheck']=df['rollingBefore']==df['rollingAfter']
        localValue=df[df['localcheck']==True]
        return localValue[['stockPrice']]
    def localConcat(self,n,stock_id="TAIEX"):
        localMax=self.getLocal(n,'max',stock_id)
        localMax['localValue']='localMax'
        localMin=self.getLocal(n,'min',stock_id)
        localMin['localValue']='localMin'
        loclaPeriod=pd.concat([localMax,localMin],axis=0).sort_index()
        return loclaPeriod
    def localPeriod(self,n,stock_id="TAIEX"):
        localPeriod=self.localConcat(n,stock_id)
        localPeriod2=pd.DataFrame([])
        tempPeriod=localPeriod.iloc[0]
        tempPrice=localPeriod['stockPrice'][0]
        for i in range(len(localPeriod)-1):
            localValue=localPeriod['localValue']
            if localValue[i]!=localValue[i+1]:
                localPeriod2=pd.concat([localPeriod2,tempPeriod],axis=1)
                tempPeriod=localPeriod.iloc[i+1]
                tempPrice=localPeriod['stockPrice'][i+1]        
            else:
                if localValue[i]=='localMin' and localPeriod['stockPrice'][i+1]<tempPrice:
                    tempPrice=localPeriod['stockPrice'][i+1]
                    tempPeriod=localPeriod.iloc[i+1]
                if localValue[i]=='localMax' and localPeriod['stockPrice'][i+1]>tempPrice:
                    tempPrice=localPeriod['stockPrice'][i+1]
                    tempPeriod=localPeriod.iloc[i+1]    
        localPeriod2=pd.concat([localPeriod2,localPeriod.iloc[-1]],axis=1)
        return localPeriod2.transpose()     
    def localPeriodDetail(self,n,stock_id="TAIEX"):
        dm=DateManage()
        localPeriod=self.localPeriod(n,stock_id)
        localPeriod['day1']=localPeriod.index
        localPeriod['day2']=localPeriod['day1'].shift(1)
        localPeriod['dayDiffer']=0
        localPeriod['increase%']=(localPeriod['stockPrice']/localPeriod['stockPrice'].shift(1)-1)*100
        for i in range(1,len(localPeriod)):
            localPeriod['dayDiffer'][i]=dm.daysDiffer(localPeriod['day1'][i],localPeriod['day2'][i])
            localPeriod['increase%'][i]=round(localPeriod['increase%'][i])
        return localPeriod[['stockPrice','localValue','dayDiffer','increase%']][1:]      
    def periodDetailToSQL(self,n=20,stock_id="TAIEX"):
        periodDetail=self.localPeriodDetail(n,stock_id).reset_index()    
        connstr=self.connstrLocalValue+'localValue'+'.db'
        conn=sqlite3.connect(connstr)
        periodDetail.to_sql('localValueP'+str(n)+'S'+stock_id,conn,if_exists='replace',index=False)
    def periodDetailFromSQL(self,n=20,stock_id="TAIEX"):
        connstr=self.connstrLocalValue+'localValue'+'.db'
        conn=sqlite3.connect(connstr)
        s="""select * from localValueP%sS%s """%(n,stock_id)
        data=pd.read_sql(s,conn)
        return data