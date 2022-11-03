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

class SeasonData(DateManage):
    def __init__(self,start_date):
        self.start_date=start_date
        self.releaseDates=["-03-31","-05-15","-08-14","-11-14"]
        self.correspondDates=["-12-31","-03-31","-06-30","-09-30"]
    def basePeriod(self):
        periodData=[]
        for i in range(4):
            periodData.append(str(super().transToDate(self.start_date).year)+self.releaseDates[i])
        return periodData
        # 最近4季發布財報時間
    def firstPeriod(self):
        self.tempPeriod=4
        self.tempData=[]
        for i in range(3):
            if super().daysDiffer(self.start_date,self.basePeriod()[i])>0 and super().daysDiffer(self.start_date,self.basePeriod()[i+1]):
                self.tempPeriod=i+1
        for j in range(self.tempPeriod,len(self.releaseDates)):
            self.tempData.append(str(super().transToDate(self.start_date).year-1)+self.releaseDates[j])
        return self.tempData+self.basePeriod()[0:self.tempPeriod]
        # 財報發布時間對應的財報日期
    def responseStatementDate(self,releaseDate):
        if super().transToDate(releaseDate).month==3:
            return str(super().transToDate(releaseDate).year-1)+self.correspondDates[0]
        elif super().transToDate(releaseDate).month==5:
            return str(super().transToDate(releaseDate).year)+self.correspondDates[1]  
        elif super().transToDate(releaseDate).month==8:
            return str(super().transToDate(releaseDate).year)+self.correspondDates[2] 
        else:
            return str(super().transToDate(releaseDate).year)+self.correspondDates[3]                   