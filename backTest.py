from data import *

class BackTest(FromSQL):
    def __init__(self):
        super().__init__()
    def fillConditionDate(self,mainData,condData,indexDate='date'):
        mainDate=list(mainData.index)
        condDate=list(condData.index)
        differDate=[]
        for date in condDate:
            if date not in mainDate:
                differDate.append(date)
        for date in differDate:
            mainData.loc[date]=0
        mainData=mainData.sort_values(indexDate)
    