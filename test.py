from crawler import TaiwanStockExchangeCrawler
import utils
import json


crawler = TaiwanStockExchangeCrawler()
with open("./json/test.json", mode="w", encoding="utf-8") as f:
    json.dump(crawler.report("個股每日股價與月平均", stock_no="2330", date_range=("20250101", "20250401")),f, ensure_ascii=False, indent=4)