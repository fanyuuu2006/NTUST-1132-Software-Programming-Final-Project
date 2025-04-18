import json
from linebot.models import SendMessage, TextSendMessage
from typing import Callable, Literal

from api.controllers import pricetrend

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
                "4️⃣ 日期沒給的話預設為今天喔💙\n"
                "5️⃣ 間隔單位 分為 day、month 預設為 day\n"
                "6️⃣ 若圖表無法顯示，請確認網路狀況或將網址貼到瀏覽器開啟試試看～\n"
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
    "/pricetrend": {
        "discription": "獲取期間內收盤價走勢圖",
        "format": "/pricetrend <股票代號> <起始日期?> <結束日期?> <間隔單位?>",
        "controller": pricetrend.controller
    },
}

def reply_handler(text: str) -> list[SendMessage]:
    """
    根據傳入的文字，取得對應的 LINE 回覆訊息。
    """
    try:
        cmd = text.split(' ')[0]
        if cmd == "/":
            return [TextSendMessage(text="/ 與 指令之間可沒有空格喔🤌")]
        if cmd.lower() not in features:
            # 若無匹配功能，則從 dialoglib.json 查找回覆
            with open("json/dialoglib.json", "r", encoding="utf-8") as f:
                dialoglib: dict = json.load(f)
                for key, value in dialoglib.items():
                    if text in key:
                        return [TextSendMessage(text=value)]
                else:
                    return [TextSendMessage(text="玩股票都不揪喔❓\n輸入 /help 來查看可用的指令！😎😎")]

        else:
            feature = features[cmd]
            try:
                messages = feature["controller"](text)
                if len(messages) > 5:
                    return [
                        TextSendMessage(text="🙇 不好意思，回覆訊息太多啦🤒"),
                        TextSendMessage(text="我最多只能回覆 5 則訊息喔！\n請您分段或精簡查詢內容🥹")
                        ]
                return messages

            except IndexError:
                return [TextSendMessage(
                    text=(
                        f"⚠️ 參數好像不太夠喔！\n\n"
                        f"📖 功能說明：{feature['discription']}\n"
                        f"🧾 正確格式：{feature['format']}\n\n"
                        f"👉 快試試看輸入正確格式吧～"
                    )
                )]
            except Exception as e:
                return [
                    TextSendMessage(
                    text=(
                        f"😵‍💫 糟糕！剛剛好像發生了錯誤...\n\n"
                        f"🔍 功能：{feature['discription']}\n"
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