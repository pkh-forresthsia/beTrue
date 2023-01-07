import requests
import pandas as pd
# try:
#     # 👇️ using Python 3.10+
#     from collections.abc import Mapping
# except ImportError:
#     # 👇️ using Python 3.10-
#     from collections import Mapping
url = "https://api.finmindtrade.com/api/v4/data"
parameter = {
    "dataset": "TaiwanStockPrice",
    "data_id": "2330",
    "start_date": "2020-04-02",
    "end_date": "2020-04-12",
    "token": "",  # 參考登入，獲取金鑰
}
resp = requests.get(url, params=parameter)
# data = resp.json()
# data = pd.DataFrame(data["data"])
# print(data)
