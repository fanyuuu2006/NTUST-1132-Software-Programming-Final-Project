from linebot.models import SendMessage, ImageSendMessage, TextSendMessage
import urllib.parse
from crawler import TaiwanStockExchangeCrawler
import utils
def controller(text: str) -> list[SendMessage]:
    """
    處理 /volumebar 指令，獲取期間內收盤價趨勢圖
    """
    # 解析使用者輸入的文字，取得股票代號
    part = text.split(" ")
    stock_no = part[1]
    start_date = part[2] if len(part) > 2 else utils.date.last_month()
    end_date = part[3] if len(part) > 3 else utils.date.today()
    interval = part[4] if len(part) > 4 else "day"
    
    stock = TaiwanStockExchangeCrawler.no(stock_no, date_range=(start_date, end_date), only_fetch=["real_time", "daily" if interval == "day" else "month_avg"])
    stock_data = stock.daily_field_transform(
        field="收盤價",
        interval=interval,
        date_range=(start_date, end_date),
        )
    
    if not stock_data:
        return [TextSendMessage(text="⚠️ 該期間內查無收盤價資料\n請確認日期或改用其他區間")]

    url = f"https://dobujio.vercel.app/plot?"\
        f"type=trend" \
        f"&title={urllib.parse.quote(stock_no + '-' + stock.get('股票簡稱')[0] + '-收盤價趨勢圖')}" \
        f"&x_label={urllib.parse.quote('日期')}" \
        f"&y_label={urllib.parse.quote('收盤價')}" \
        f"&token={utils.data.compress_data(stock_data)}"
        
    if len(url) > 2000:
        raise ValueError("❗資料量過大，超過圖表產生限制，請縮短日期範圍或區間方式再試一次 🙏")
        
    return [
    TextSendMessage(
        text=(
            f"📈 指定股票收盤價趨勢圖查詢\n"
            f"📌 股票代號：{stock_no}\n"
            f"📅 日期區間：{start_date} ~ {end_date}\n"
            f"🔗 趨勢圖連結：{utils.url.shorten_url(url)}"
        )
    ),
    ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
    )
]