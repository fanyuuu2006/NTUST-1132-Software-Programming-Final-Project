from linebot.models import SendMessage, ImageSendMessage, TextSendMessage
from crawler import TaiwanStockExchangeCrawler
import utils
def controller(text: str) -> list[SendMessage]:
    """
    處理 /pricetrend 指令，獲取期間內指定股票之成交量長條圖
    """
    # 解析使用者輸入的文字，取得股票代號
    part = text.split(" ")
    stock_no = part[1]
    start_date = part[2] if len(part) > 2 else utils.date.last_month()
    end_date = part[3] if len(part) > 3 else utils.date.today()
    interval = part[4] if len(part) > 4 else "day"
    
    stock = TaiwanStockExchangeCrawler.no(stock_no, date_range=(start_date, end_date), only_fetch=["daily", "real_time"] )
    stock_data = stock.daily_field_transform(
        field="成交筆數",
        interval=interval,
        date_range=(start_date, end_date),
        )
        
    url = utils.url.generate_plot_url(
        type="bar",
        title=stock_no + '-' + stock.get('股票簡稱')[0] + '-成交量長條圖',
        x_label='日期',
        y_label='成交量',
        token= utils.data.compress_data(stock_data)
        )
        
    if len(url) > 2000:
        raise ValueError("❗資料量過大，超過圖表產生限制，請縮短日期範圍或區間方式再試一次 🙏")
        
    return [
    TextSendMessage(
        text=(
            f"📈 指定股票成交量長條圖查詢\n"
            f"📌 股票代號：{stock_no}\n"
            f"📅 日期區間：{start_date} ~ {end_date}\n"
            f"🔗 長條圖連結：{utils.url.shorten_url(url)}"
        )
    ),
    ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
    )
]