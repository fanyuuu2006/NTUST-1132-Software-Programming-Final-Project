import json
from linebot.models import SendMessage, TextSendMessage
from typing import Callable, Literal
from crawler import TaiwanStockExchangeCrawler


FeatureHandler = Callable[[str], list[SendMessage]]


features: dict[str, dict[Literal["discription", "handler"], str | FeatureHandler]] = {  
    "/test": {
        "discription": "測試用指令",
        "handler": lambda _: [
            TextSendMessage(
                text="測試都不揪喔❓😎"
            )
        ]
    },
    "/help": {
        "discription": "顯示所有指令",
        "handler": lambda _: [
            TextSendMessage(
                text="\n".join([f"{cmd} - {data['discription']}" for cmd, data in features.items() if cmd != "/help"])
            )
        ]
    },
    "/name": {
        "discription": "查詢股票名稱：/name {股票代號}",
        "handler": lambda text: [
            TextSendMessage(text=f"🔍 股票代號 {text.split(' ')[1]} 是：{TaiwanStockExchangeCrawler.no(text.split(' ')[1]).get('股票全名')}")
        ]
    },
    "/price": {
        "discription": "查詢即時股價：/price {股票代號}",
        "handler": lambda text: [
            TextSendMessage(text=f"📈 即時成交金額：{TaiwanStockExchangeCrawler.no(text.split(' ')[1]).get('目前成交價')}")
        ]
    }
}

def text_handler(text: str) -> list[SendMessage]:
    """
    根據傳入的文字，取得對應的 LINE 回覆訊息。
    """
    try:
        cmd = text.split(' ')[0]
        if cmd in features:
            feature = features[cmd]
            try:
                return feature["handler"](text)
            except Exception as e:
                return [TextSendMessage(text=f"❌ 指令處理失敗：{e}\n{feature['discription']}")]
    except Exception as e:
        return [TextSendMessage(text=f"❌ 發生錯誤了...\n{e}"), TextSendMessage(text="請確認指令格式是否正確！\n輸入 /help 來查看可用的指令！😎😎")]

    # 若無匹配功能，則從 dialoglib.json 查找回覆
    with open("json/dialoglib.json", "r", encoding="utf-8") as f:
        dialoglib: dict = json.load(f)
        if text in dialoglib:
            return [TextSendMessage(text=dialoglib[text])]
        else:
            return [TextSendMessage(text="玩股票都不揪喔❓\n輸入 /help 來查看可用的指令！😎😎")]
