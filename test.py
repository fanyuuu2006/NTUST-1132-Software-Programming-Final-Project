import json
from crawler import TaiwanStockExchangeCrawler
import urllib.parse
import utils


stock_no = "2330"
start_date = "20240101"
end_date = "20250419"
interval = "day"
stock = TaiwanStockExchangeCrawler.no(stock_no, date_range=(start_date, end_date))
stock_data = stock.daily_field_transform(
    field="收盤價",
    interval=interval,
    date_range=(start_date, end_date),
    )



url = f"https://dobujio.vercel.app/plot?title={urllib.parse.quote(stock_no + '-' + stock.get('股票簡稱')[0] + '-收盤價趨勢圖')}" \
      f"&x_label={urllib.parse.quote('日期')}" \
      f"&y_label={urllib.parse.quote('收盤價')}" \
      f"&data={urllib.parse.quote(json.dumps(stock_data, ensure_ascii=False))}"

print(utils.url.shorten_url(url))
# with open("./json/test.json", "w", encoding="utf-8") as f:
#     f.write(json.dumps(utils.date.month_range(start=start_date, end=end_date), ensure_ascii=False, indent=4))