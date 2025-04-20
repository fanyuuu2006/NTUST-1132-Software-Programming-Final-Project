import json
from linebot.models import (
    SendMessage,
    TextSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction
)
from typing import Callable, Literal

from api.controllers import pricetrend

from .controllers import name, price, daily, kline, volumebar


FeatureHandler = Callable[[str], list[SendMessage]]


features: dict[str, dict[Literal["description", "format", "controller"], str | FeatureHandler]] = {  
    "/help": {
        "description": "顯示所有指令",
        "format": "/help",
        "controller": lambda _: [
            TextSendMessage(
            text="📖 指令列表\n\n" + "\n\n".join([
                f"🟢{data['description']}\n📌{data['format']}" for cmd, data in features.items() if cmd != "/help"
            ])
        ),
            TextSendMessage(
                    text=(
                "❗小提醒：\n"
                "1️⃣ 指令與參數要以空格區隔！\n"
                "2️⃣`?` 代表 可選參數 ，不一定要填寫唷！😘\n"
                "3️⃣ 日期格式為 `YYYYMMDD`，例如：20250417\n"
                "4️⃣ 日期沒給的話預設為今天喔💙\n"
                "5️⃣ 間隔單位 分為 day、month 預設為 day\n"
                "6️⃣ 若圖表無法顯示，請確認網路狀況或將網址貼到瀏覽器開啟試試看～\n"
            )
        )
        ]
    },
    "/test": {
        "description": "測試用指令",
        "format": "/test",
        "controller": lambda _: [
            TextSendMessage(
                text="🧪 測試成功！\n測試都不揪喔❓😎"
            )
        ]
    },
    "/echo": {
        "description": "回傳你輸入的訊息內容（測試用）",
        "format": "/echo <訊息>",
        "controller": lambda text: [
        TextSendMessage(
            text="你說的是：" + text.partition(" ")[2]
            )
        ]
    },
    "/name": {
        "description": "查詢股票名稱",
        "format": "/name <股票代號>",
        "controller": name.controller
    },
    "/price": {
        "description": "查詢即時股價",
        "format": "/price <股票代號>",
        "controller": price.controller
    },
    # 加入 features 中：
    "/daily": {
        "description": "查詢期間內每日交易資訊",
        "format": "/daily <股票代號> <起始日期?> <結束日期?>",
        "controller": daily.controller
    },
    "/pricetrend": {
        "description": "獲取期間內指定股票之收盤價趨勢圖",
        "format": "/pricetrend <股票代號> <起始日期?> <結束日期?> <間隔單位?>",
        "controller": pricetrend.controller
    },
    "/kline": {
        "description": "獲取期間內指定股票之K線圖",
        "format": "/kline <股票代號> <起始日期?> <結束日期?>",
        "controller": kline.controller
    },
    "/volumebar": {
        "description": "獲取期間內指定股票之成交量長條圖",
        "format": "/volumebar <股票代號> <起始日期?> <結束日期?> <間隔單位?>",
        "controller": volumebar.controller
    },
}

def reply_handler(text: str) -> list[SendMessage]:
    """
    根據傳入的文字，取得對應的 LINE 回覆訊息。
    """
    try:
        cmd = text.split(' ')[0].lower()
        if cmd == "/":
            return [TextSendMessage(text="⚠️ `/` 與 指令之間可沒有空格喔🤌")]
        if cmd not in features:
            if cmd.startswith("/"):
                candidates = [c for c in features if c.startswith(cmd)] 
            if len(candidates) > 0:
                return [TextSendMessage(
                    text="🧠 你是不是想打這些指令❓",
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=MessageAction(label=c, text=c))
                            for c in candidates[:5]
                        ]
                    )
                )]
            
            # 若無匹配功能，則從 dialoglib.json 查找回覆
            with open("json/dialoglib.json", "r", encoding="utf-8") as f:
                dialoglib: dict = json.load(f)
                for key, value in dialoglib.items():
                    if  key in text:
                        return [TextSendMessage(text=value)]

            return [TextSendMessage(text="玩股票都不揪喔❓\n輸入 /help 來查看可用的指令！😎😎")]

        else:
            feature = features[cmd]
            try:
                messages = feature["controller"](text)
                if len(messages) > 5:
                    return [
                        TextSendMessage(text="🙇 不好意思，要回覆太多訊息啦🤒"),
                        TextSendMessage(text="我一次最多只能回覆 5 則訊息喔！\n請您分段或精簡查詢內容🥹")
                        ]
                return messages

            except IndexError:
                return [TextSendMessage(
                    text=(
                        f"⚠️ 參數好像不太夠喔！\n\n"
                        f"📖 功能說明：{feature['description']}\n"
                        f"🧾 正確格式：{feature['format']}\n\n"
                        f"👉 快試試看輸入正確格式吧～"
                    )
                )]
            except Exception as e:
                return [
                    TextSendMessage(
                    text=(
                        f"😵‍💫 糟糕！剛剛好像發生了錯誤...\n\n"
                        f"🔍 功能：{feature['description']}\n"
                        f"📛 錯誤內容：{str(e)}"
                    )),
                    TextSendMessage(
                        text=(
                            f"你可以稍後再試，或回報問題給開發者 🙇\n"
                            f"開發者的聯絡方式：\n"
                            f"https://www.instagram.com/fan._.yuuu/\n"
                            f"（請附上錯誤內容）"
                        ))
                ]
    except Exception as e:
        return [
        TextSendMessage(text=f"❌ 發生錯誤了...\n📛 錯誤內容：{e}"),
        TextSendMessage(text="請檢查指令輸入格式！\n輸入 /help 查看可用指令 😎")
    ]