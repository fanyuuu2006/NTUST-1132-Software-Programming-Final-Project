from crawler import TaiwanStockExchangeCrawler
from linebot.models import SendMessage, TextSendMessage

def handler(text: str) -> list[SendMessage]:
    """
    處理 /name 指令，查詢股票名稱
    """
    # 解析使用者輸入的文字，取得股票代號
    stock_no = text.split(" ")[1]

    # 查詢股票名稱
    stock_name = TaiwanStockExchangeCrawler.no(stock_no).get("股票全名")[0]

    # 回覆訊息列表
    return [
            TextSendMessage(
                text=(
                    f"🔍 查詢股票名稱\n"
                    f"📌 股票代號：{stock_no}\n"
                    f"📘 股票名稱：{stock_name}"
                )
            )
        ]
    