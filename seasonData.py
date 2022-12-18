from data import *
from sympy import *

class SeasenData(FromSQL):
    def __init__(self):
        super().__init__()    
        self.yearSeason=4
class StatementData(SeasenData):
    def __init__(self):
        super().__init__()   
        self.statement=self.datasetFromSQL("TaiwanStockFinancialStatements")
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
    def estimatePrice(self,eps,growth1,growth2=0.02,g=0.02,e=0.1):
        r=(1+g)/(1+e)
        tempSum=0
        for i in range(10):
            if i<5:
                eps=eps*((1+growth1)/(1+e))
                tempSum=tempSum+eps
            else:
                eps=eps*((1+growth2)/(1+e))
                tempSum=tempSum+eps
        eps=eps*r/(1-r)
        tempSum=tempSum+eps
        return tempSum
    def nYearIncrease(self,n,table):
        dt=DataTrans()
        dt.nPeriodIncrease(n*4,table,4).iloc[-1]