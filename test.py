from crawler import TaiwanStockExchangeCrawler
import utils
import json


crawler = TaiwanStockExchangeCrawler()
with open("./json/test.json", mode="w", encoding="utf-8") as f:
    json.dump(crawler.report("個股每日平均股價、成交量等", (utils.date.today(), utils.date.today()), "2330"),f, ensure_ascii=False, indent=4)