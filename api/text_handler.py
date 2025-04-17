import json
from linebot.models import SendMessage, TextSendMessage
from typing import Callable, Literal

from .controllers import name, test, price, daily


FeatureHandler = Callable[[str], list[SendMessage]]


features: dict[str, dict[Literal["discription", "format", "controller"], str | FeatureHandler]] = {  
    "/help": {
        "discription": "顯示所有指令",
        "format": "/help",
        "controller": lambda _: [
            TextSendMessage(
            text="📖 指令列表\n\n" + "\n\n".join([
                f"🟢{data['discription']}\n📌{data['format']}" for cmd, data in features.items() if cmd != "/help"
            ])
        ),
            TextSendMessage(
                    text=(
                "❗小提醒：\n"
                "1️⃣ 指令與參數要以空格區隔！\n"
                "2️⃣`?` 代表 可選參數 ，不一定要填寫唷！😘\n"
                "3️⃣ 日期格式為 `YYYYMMDD`，例如：20250417\n"
            )
        )
        ]
    },
    "/test": {
        "discription": "測試用指令",
        "format": "/test",
        "controller": test.controller
    },
    "/name": {
        "discription": "查詢股票名稱",
        "format": "/name <股票代號>",
        "controller": name.controller
    },
    "/price": {
        "discription": "查詢即時股價",
        "format": "/price <股票代號>",
        "controller": price.controller
    },
    # 加入 features 中：
    "/daily": {
        "discription": "查詢期間內每日交易資訊",
        "format": "/daily <股票代號> <起始日期?> <結束日期?>",
        "controller": daily.controller
    },
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
                return feature["controller"](text)
            except IndexError:
                return [TextSendMessage(
                    text=f"❌ 指令參數不足\n📖 說明：{feature['discription']}\n💡 範例：{feature['format']}"
                )]
            except Exception as e:
                return [TextSendMessage(
                    text=f"❌ 發生錯誤：{str(e)}\n📖 功能：{feature['discription']}"
                )]
    except Exception as e:
        return [
        TextSendMessage(text=f"❌ 發生錯誤了...\n📛 錯誤內容：{e}"),
        TextSendMessage(text="請檢查指令輸入格式！\n輸入 /help 查看可用指令 😎")
    ]
    # 若無匹配功能，則從 dialoglib.json 查找回覆
    with open("json/dialoglib.json", "r", encoding="utf-8") as f:
        dialoglib: dict = json.load(f)
        if text in dialoglib:
            return [TextSendMessage(text=dialoglib[text])]
        else:
            return [TextSendMessage(text="玩股票都不揪喔❓\n輸入 /help 來查看可用的指令！😎😎")]
