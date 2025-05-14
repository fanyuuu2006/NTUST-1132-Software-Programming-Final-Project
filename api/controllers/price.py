from crawler import TaiwanStockExchangeCrawler
from linebot.models import SendMessage, TextSendMessage

def controller(text: str) -> list[SendMessage]:
    """
    處理 /price 指令，查詢股票即時價格
    """
    # 解析使用者輸入的文字，取得股票代號
    part = text.split(" ")
    stock_no = part[1]

    # 查詢即時價格
    try:
        stock_price = round(float(TaiwanStockExchangeCrawler.no(stock_no, only_fetch=["real_time"]).get("目前成交價")[0]), 2)
    except ValueError as e:
        if "-" in str(e):
            return [
                TextSendMessage(text="⚠️ 無法取得即時股價，可能是輸入錯誤、未開盤或今日無交易。")
                ]
        else:
            raise ValueError(e)
    # 回覆訊息列表
    return [
            TextSendMessage(
                    text=(
                        f"📈 即時股價查詢\n"
                        f"📌 股票代號：{stock_no}\n"
                        f"💰 目前成交價：{stock_price:.2f}"
                    )
                )
            ]