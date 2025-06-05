from crawler import TaiwanStockExchangeCrawler
import utils

text="/kline 2330 20250101 20250418"

part = text.split(" ")
stock_no = part[1]
start_date = part[2] if len(part) > 2 else utils.date.last_month()
end_date = part[3] if len(part) > 3 else utils.date.today()

stock = TaiwanStockExchangeCrawler.no(stock_no, date_range=(start_date, end_date), only_fetch=["real_time","daily"])
stock_data = stock.kline(
    date_range=(start_date, end_date),
    )
    
url = utils.url.generate_plot_url(
    type="kline",
    title=stock_no + '-' + stock.get('股票簡稱')[0] + '-K線圖',
    token= utils.data.compress_data(stock_data)
    )
print(utils.url.shorten_url(url))  # print the url of the plot