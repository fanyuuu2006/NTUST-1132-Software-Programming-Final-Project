from crawler import TaiwanStockExchangeCrawler
import json
import urllib.parse
import utils


# crawler = TaiwanStockExchangeCrawler()

# with open("./json/test.json", mode="w", encoding="utf-8") as file:
#     file.write(json.dumps(crawler.report("個股每日歷史交易資料", ("20250401", "20250418"), "2408"), ensure_ascii=False, indent=4))

stock_no = "1435"
start_date = "20240801"
end_date = "20250419"
interval = "day"
stock = TaiwanStockExchangeCrawler.no(stock_no)
# stock_data = stock.daily_field_transform(
#     field="成交金額",
#     interval=interval,
#     date_range=(start_date, end_date),
#     )



# url = f"https://dobujio.vercel.app/plot?"\
#     f"type=bar" \
#     f"&title={urllib.parse.quote(stock_no + '-' + stock.get('股票簡稱')[0] + '-成交量長條圖')}" \
#     f"&x_label={urllib.parse.quote('日期')}" \
#     f"&y_label={urllib.parse.quote('成交量')}" \
#     f"&token={utils.data.compress_data(stock_data)}"

stock_data = stock.kline(
    # date_range=(start_date, end_date),
)

url = f"https://dobujio.vercel.app/plot?"\
    f"type=kline" \
    f"&title={urllib.parse.quote(stock_no + '-' + stock.get('股票簡稱')[0] + '-K線圖')}" \
    f"&token={utils.data.compress_data(stock_data)}"


print(utils.url.shorten_url(url))
# print(utils.url.shorten_url(url))
