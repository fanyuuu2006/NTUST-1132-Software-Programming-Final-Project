from crawler import TaiwanStockExchangeCrawler
import urllib.parse
import utils


stock_no = "2330"
start_date = "20250101"
end_date = "20250419"
interval = "day"
stock = TaiwanStockExchangeCrawler.no(stock_no, date_range=(start_date, end_date))
stock_data = stock.daily_field_transform(
    field="成交筆數",
    interval=interval,
    date_range=(start_date, end_date),
    )



url = f"https://dobujio.vercel.app/plot?"\
    f"type=bar" \
    f"&title={urllib.parse.quote(stock_no + '-' + stock.get('股票簡稱')[0] + '-成交量長條圖')}" \
    f"&x_label={urllib.parse.quote('日期')}" \
    f"&y_label={urllib.parse.quote('成交量')}" \
    f"&token={utils.data.compress_data(stock_data)}"

# stock_data = stock.kline(
#     date_range=(start_date, end_date),
# )

# url = f"https://dobujio.vercel.app/plot?"\
#     f"type=kline" \
#     f"&title={urllib.parse.quote(stock_no + '-' + stock.get('股票簡稱')[0] + '-K線圖')}" \
#     f"&token={utils.data.compress_data(stock_data)}"


print(utils.url.shorten_url(url))
# print(utils.url.shorten_url(url))
