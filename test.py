from crawler import TaiwanStockExchangeCrawler
import utils
import json
import requests 


data = TaiwanStockExchangeCrawler.report("個股每日歷史交易資料",stock_no=2330, date_range=("20241201", None))

s = utils.data.compress_data(data)

print(s)