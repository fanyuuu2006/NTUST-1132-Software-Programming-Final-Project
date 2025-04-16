import json
from linebot.models import SendMessage, TextSendMessage
from typing import Callable, Literal
from crawler import TaiwanStockExchangeCrawler

# 功能與關鍵字設定
features: dict[str, dict[Literal["keyword", "handler"], list[str]] | Callable[[str], list[SendMessage]]] = {
    "根據代號查詢股票名稱": {
        "keyword": ["查", "查詢股票", "查詢", "查股票", "代號", "股票代號"],
        "handler": lambda text: [
            TextSendMessage(text=TaiwanStockExchangeCrawler.no(text.split(" ")[0]).get_name())
        ]
    },
    "查詢即時股價": {
    "keyword": ["股價", "價格", "現在多少", "現在價格"],
    "handler": lambda text: [
        TextSendMessage(text=TaiwanStockExchangeCrawler.no(text.split(" ")[0]).get("成交金額"))
    ]
},
    "查詢歷史股價": {
        "keyword": ["歷史", "歷史股價", "過去", "過去股價"],
        "handler": lambda text: [
            TextSendMessage(text=TaiwanStockExchangeCrawler.no(text.split(" ")[0]).get_history())
        ]
    },
    "查詢法人買賣超": {
        "keyword": ["法人", "法人買賣超", "三大法人"],
        "handler": lambda text: [
            TextSendMessage(text=TaiwanStockExchangeCrawler.no(text.split(" ")[0]).get_institutional_investors())
        ]
    },
    "查詢成交量": {
        "keyword": ["成交量", "成交", "交易量"],
        "handler": lambda text: [
            TextSendMessage(text=TaiwanStockExchangeCrawler.no(text.split(" ")[0]).get_transaction_volume())
        ]
    },
}

def text_handler(text: str) -> list[SendMessage]:
    """
    根據傳入的文字，取得對應的 LINE 回覆訊息。
    """
    try:
        for feature, data in features.items():
            if any(keyword in text for keyword in data["keyword"]):
                return data["handler"](text)
    except Exception as e:
        return [TextSendMessage(text=f"❌ 發生錯誤了...\n{e}")]

    # 若無匹配功能，則從 dialoglib.json 查找回覆
    with open("json/dialoglib.json", "r", encoding="utf-8") as f:
        dialoglib: dict = json.load(f)
        if text in dialoglib:
            return [TextSendMessage(text=dialoglib[text])]
        else:
            return [TextSendMessage(text="玩股票都不揪喔❓你今天想幹嘛呢\n😎")]
