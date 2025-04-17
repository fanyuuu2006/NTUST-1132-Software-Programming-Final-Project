import json
from linebot.models import SendMessage, TextSendMessage
from typing import Callable, Literal
from crawler import TaiwanStockExchangeCrawler


FeatureHandler = Callable[[str], list[SendMessage]]


features: dict[str, dict[Literal["discription", "format", "handler"], str | FeatureHandler]] = {  
    "/test": {
        "discription": "測試用指令",
        "format": "/test",
        "handler": lambda _: [
            TextSendMessage(
                text="🧪 測試成功！\n測試都不揪喔❓😎"
            )
        ]
    },
    "/help": {
        "discription": "顯示所有指令",
        "format": "/help",
        "handler": lambda _: [
            TextSendMessage(
            text="📖 指令列表\n\n" + "\n\n".join([
                f"🟢 {cmd}: {data['discription']}\n　📌{data['format']}" for cmd, data in features.items() if cmd != "/help"
            ])
        )
        ]
    },
    "/name": {
        "discription": "查詢股票名稱",
        "format": "/name <股票代號>",
        "handler": lambda text: [
            TextSendMessage(
                text=(
                    f"🔍 查詢股票名稱\n"
                    f"📌 股票代號：{text.split(' ')[1]}\n"
                    f"📘 股票名稱：{TaiwanStockExchangeCrawler.no(text.split(' ')[1]).get('股票全名')[0]}"
                )
            )
        ]
    },
    "/price": {
        "discription": "查詢即時股價",
        "format": "/price <股票代號>",
        "handler": lambda text: [
            TextSendMessage(
                    text=(
                        f"📈 即時股價查詢\n"
                        f"📌 股票代號：{text.split(' ')[1]}\n"
                        f"💰 目前成交價：{round(float(TaiwanStockExchangeCrawler.no(text.split(' ')[1]).get('目前成交價')[0]), 2):.2f}"
                    )
                )
            ]
    },
    "/info": {
        "discription": "查詢股票相關資訊",
        "format": "/info <股票代號> <欄位名稱>",
        "handler": lambda text: [
            TextSendMessage(
                text=(
                    f"📊 股票資訊查詢\n"
                    f"📌 股票代號：{text.split(' ')[1]}\n"
                    f"📘 {text.split(' ')[2]}：{TaiwanStockExchangeCrawler.no(text.split(' ')[1]).get(text.split(' ')[2])[0]}"
                )
            )
        ] if len(text.split(' ')) > 2 else [
            TextSendMessage(
                text=(
                    f"📊 股票資訊查詢\n"
                    f"📌 股票代號：{text.split(' ')[1]}\n"
                    f"📘 股票資訊：\n" +
                    "\n\n".join([
                        f"　📌 {key}: {value[0]}" for key, value in TaiwanStockExchangeCrawler.no(text.split(' ')[1]).get_data().items() if key != "每日交易資料"
                    ]) +
                    f"\n\n每日交易資料：\n" +
                    "\n\n".join([
                        f"　📌 {key}: {value[0]}" for data in TaiwanStockExchangeCrawler.no(text.split(' ')[1]).get("每日交易資料") for key, value in data.items()
                    ])
                )
            )
        ]
    }
}

def text_handler(text: str) -> list[SendMessage]:
    """
    根據傳入的文字，取得對應的 LINE 回覆訊息。
    """
    try:
        cmd = text.split(' ')[0]
        if cmd.lower() in features:
            feature = features[cmd]
            try:
                return feature["handler"](text)
            except Exception as e:
                return [TextSendMessage(text=f"❌ 指令處理失敗：\n{feature['discription']}\n{e}")]
    except Exception as e:
        return [
        TextSendMessage(text=f"❌ 發生錯誤了...\n📛 錯誤內容：{e}"),
        TextSendMessage(text="請確認指令格式是否正確！\n輸入 /help 查看可用指令 😎")
    ]
    # 若無匹配功能，則從 dialoglib.json 查找回覆
    with open("json/dialoglib.json", "r", encoding="utf-8") as f:
        dialoglib: dict = json.load(f)
        if text in dialoglib:
            return [TextSendMessage(text=dialoglib[text])]
        else:
            return [TextSendMessage(text="玩股票都不揪喔❓\n輸入 /help 來查看可用的指令！😎😎")]
