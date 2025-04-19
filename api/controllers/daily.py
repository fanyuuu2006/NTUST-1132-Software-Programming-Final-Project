from crawler import TaiwanStockExchangeCrawler
import utils
from linebot.models import SendMessage, TextSendMessage
from crawler.models import DAILY_DATA_KEYS


def controller(text: str) -> list[SendMessage]:
    """
    處理 /daily 指令，查詢期間內每日交易資訊（成交量/收盤價等）
    """
    parts = text.strip().split()

    stock_no = parts[1]
    start_date = parts[2] if len(parts) > 2 else utils.date.today()
    end_date = parts[3] if len(parts) > 3 else utils.date.today()

    # 查詢每日資料
    stock = TaiwanStockExchangeCrawler.no(stock_no, date_range=(start_date, end_date))
    daily_data: list[dict[DAILY_DATA_KEYS, str]] = stock.get("每日交易資料", date_range=(start_date, end_date))[0]

    if not daily_data:
        return [TextSendMessage(text="查無資料，請確認股票代號與日期是否正確 ✅")]

    # 整理文字內容
    result: list[SendMessage] = []
    header = f"📊 股票代碼: {stock_no} ({stock.get("股票簡稱")[0]})\n（{start_date} ~ {end_date}\n每日交易資訊如下：\n"
    result.append(TextSendMessage(text=header))
    group_text = ""
    for i, day_data in enumerate(daily_data):
        group_text += (
            f"📅 日期：{utils.date.datetime.strptime(day_data['日期'], "%Y/%m/%d")}\n"
            f"📈 開盤：{day_data['開盤價']} 元\n"
            f"🔼 最高：{day_data['最高價']} 元\n"
            f"🔽 最低：{day_data['最低價']} 元\n"
            f"🔚 收盤：{day_data['收盤價']} 元\n"
            f"💵 成交金額：{day_data['成交金額']} 元\n"
            f"📦 成交股數：{day_data['成交股數']}\n"
            f"📄 成交筆數：{day_data['成交筆數']}\n"
            f"📉 漲跌：{day_data['漲跌價差']}\n"
            "———————————————\n\n"
        )
        
        if i % 5 == 0 or i == len(daily_data):
            result.append(TextSendMessage(text=group_text))
            group_text = ""

    return result
