import json
from linebot.models import SendMessage, ImageSendMessage
import urllib.parse
from crawler import TaiwanStockExchangeCrawler
import utils
def controller(text: str) -> list[SendMessage]:
    """
    處理 /pricetrend 指令，獲取期間內收盤價走勢圖
    """
    # 解析使用者輸入的文字，取得股票代號
    part = text.split(" ")
    stock_no = part[1]
    start_date = part[2] if len(part) > 2 else utils.date.today()[:6]+"01"
    end_date = part[3] if len(part) > 3 else utils.date.today()
    interval = part[4] if len(part) > 4 else "day"
    
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
    return [
            ImageSendMessage(
                    original_content_url=url,
                    preview_image_url=url
                )
            ]