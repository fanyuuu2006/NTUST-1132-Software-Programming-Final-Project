from crawler import TaiwanStockExchangeCrawler
import utils
import json


crawler = TaiwanStockExchangeCrawler()
with open("./json/test.json", mode="w", encoding="utf-8") as f:
    json.dump(crawler.report("個股每日歷史交易資料", stock_no= "2330"),f, ensure_ascii=False, indent=4)