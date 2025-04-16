import crawler
import json
# print(crawler.TaiwanStockExchangeCrawler.no("2330").get("股票全名"))
print(json.dumps(crawler.TaiwanStockExchangeCrawler.no("2330").get_data(),ensure_ascii=False, indent=4))