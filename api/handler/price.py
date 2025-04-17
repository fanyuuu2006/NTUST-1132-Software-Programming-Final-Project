from crawler import TaiwanStockExchangeCrawler
from linebot.models import SendMessage, TextSendMessage

def handler(text: str) -> list[SendMessage]:
    """
    處理 /price 指令，查詢股票即時價格
    """
    # 解析使用者輸入的文字，取得股票代號
    stock_no = text.split(" ")[1]

    # 查詢即時價格
    stock_price = TaiwanStockExchangeCrawler.no(stock_no).get("目前成交價")[0]

    # 回覆訊息列表
    return [
            TextSendMessage(
                    text=(
                        f"📈 即時股價查詢\n"
                        f"📌 股票代號：{stock_no}\n"
                        f"💰 目前成交價：{round(float(stock_price), 2):.2f}"
                    )
                )
            ]