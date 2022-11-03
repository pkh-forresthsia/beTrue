from basic import *

class Info(Param):
    def __init__(self):
        super().__init__()
        self.parameter['dataset']="TaiwanStockFinancialStatements"
    def getAll(self,start_date):
        self.parameter['start_date']=start_date
        return super().getData(self.parameter)
