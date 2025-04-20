from crawler import TaiwanStockExchangeCrawler
import utils
import json


crawler = TaiwanStockExchangeCrawler()
with open("./json/example/stock_data.json", mode="w", encoding="utf-8") as f:
    json.dump(crawler.no(stock_no="2330", date_range=("20250101", "20250401")).get_data(),f, ensure_ascii=False, indent=4)