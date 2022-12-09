import datetime
from dateutil.relativedelta import relativedelta

class DateManage():
    # 今天的日期
    def todayDate(self):
        return datetime.date.today()
    # 轉化成日期
    def transToDate(self,dateString):
        return datetime.datetime.strptime(dateString,'%Y-%m-%d')
    # 日期轉為文字    
    def transToString(self,date):
        return date.strftime('%Y-%m-%d')
    # 一個月的第一天
    def firstDay(self,dateString):
        return  self.transToDate(dateString).replace(day=1)
    # n年前的今天
    def nYearBefore(self,dateString,n):
        return (self.transToDate(dateString)-relativedelta(years=n)).strftime('%Y-%m-%d')
    def nMonthBefore(self,dateString,n):
        return (self.transToDate(dateString)-relativedelta(months=n)).strftime('%Y-%m-%d')
    def daysDiffer(self,days1,days2):
        return (self.transToDate(days1)-self.transToDate(days2)).days 
    def seasonRelease(self,dateStr):
        date=self.transToDate(dateStr)
        if date.month==3:
            return str(date.year)+"-05-15"
        elif date.month==6:
            return str(date.year)+"-08-14"
        elif date.month==9:
            return str(date.year)+"-11-14"
        else:
            return str(date.year-1)+"-03-31"   