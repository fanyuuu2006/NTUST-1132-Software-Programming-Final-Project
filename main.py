import crawler
import visualize
import line_bot

c = crawler.TaiwanStockExchangeCrawler()
stock = c.get_stock_by_no("2330")  # 台積電
visualize.plot_stock_trend(stock, "成交金額", date_range=("114/04/07", "114/04/15"))
