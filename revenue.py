from basic import *
import sqlite3
import sys

sys.path.insert(0,'../data')

class MonthInfo(Param):
    def __init__(self):
        super().__init__()
        self.parameter['dataset']="TaiwanStockMonthRevenue"
        self.revenue=sqlite3.connect('revenueData.sqlite3')
    def getAll(self,start_date):
        self.parameter['start_date']=start_date
        return super().getData(self.parameter)    
    def nYearRevenue(self,start_date,n):
        dm=DateManage()
        startDate=dm.transToString(dm.firstDay(start_date))
        for i in range(n*12):
            thisMonth=dm.nMonthBefore(startDate,i)
            thisRevenue=self.getAll(thisMonth)
            thisRevenue.to_sql('revenue'+thisMonth.replace('-','s'),self.revenue,if_exists='replace')