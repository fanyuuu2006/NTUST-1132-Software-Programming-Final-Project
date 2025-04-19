from crawler import TaiwanStockExchangeCrawler
import urllib.parse
import utils


stock_no = "2330"
start_date = "20250101"
end_date = "20250419"
interval = "day"
stock = TaiwanStockExchangeCrawler.no(stock_no, date_range=(start_date, end_date))
# stock_data = stock.daily_field_transform(
#     field="收盤價",
#     interval=interval,
#     date_range=(start_date, end_date),
#     )



# url = f"https://dobujio.vercel.app/plot?"\
#     f"type=trend" \
#     f"&title={urllib.parse.quote(stock_no + '-' + stock.get('股票簡稱')[0] + '-收盤價趨勢圖')}" \
#     f"&x_label={urllib.parse.quote('日期')}" \
#     f"&y_label={urllib.parse.quote('收盤價')}" \
#     f"&token={utils.data.compress_data(stock_data)}"

stock_data = stock.kline(
    date_range=(start_date, end_date),
)

url = f"https://dobujio.vercel.app/plot?"\
    f"type=kline" \
    f"&title={urllib.parse.quote(stock_no + '-' + stock.get('股票簡稱')[0] + '-股價K線圖')}" \
    f"&token={utils.data.compress_data(stock_data)}"


print(utils.url.shorten_url(url))
# print(utils.url.shorten_url(url))
