from crawler import TaiwanStockExchangeCrawler
import utils
import json




crawler = TaiwanStockExchangeCrawler()
with open("./json/test.json", mode="w", encoding="utf-8") as f:
    json.dump(crawler.report("每日收盤行情"),f, ensure_ascii=False, indent=4)