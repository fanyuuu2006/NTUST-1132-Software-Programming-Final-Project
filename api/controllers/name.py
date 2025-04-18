from crawler import TaiwanStockExchangeCrawler
from linebot.models import SendMessage, TextSendMessage

def controller(text: str) -> list[SendMessage]:
    """
    處理 /name 指令，查詢股票名稱
    """
    # 解析使用者輸入的文字，取得股票代號
    part = text.split(" ")
    stock_no = part[1]
    
    stock = TaiwanStockExchangeCrawler.no(stock_no)

    # 查詢股票名稱
    stock_full_name = stock.get("股票全名")[0]
    stock_short_name = stock.get("股票簡稱")[0] if stock.get("股票簡稱") else "無資料"
    
    # 回覆訊息列表
    return [
            TextSendMessage(
                text=(
                    f"🔍 查詢股票名稱\n"
                    f"📌 股票代號：{stock_no}\n"
                    f"🏢 股票名稱：{stock_full_name}\n"
                    f"📘 股票簡稱：{stock_short_name}"
                )
            )
        ]
    