import json
from linebot.models import (
    SendMessage,
    TextSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction
)

from .features import features

def reply_handler(text: str) -> list[SendMessage]:
    """
    根據傳入的文字，取得對應的 LINE 回覆訊息。
    """
    try:
        cmd = text.split(' ')[0].lower()
        if cmd == "/":
            return [TextSendMessage(text="⚠️ `/` 與 指令之間可沒有空格喔🤌")]
        if cmd in features:
            feature = features[cmd]
            try:
                messages = feature["controller"](text)
                if len(messages) > 5:
                    return messages[:4] + [
                        TextSendMessage(text=(
                            f"不好意思🙇\n"\
                            f"我一次最多只能回覆 5 則訊息喔！\n"\
                            f"部分訊息已被截斷了！\n"\
                            f"請您分段或精簡查詢內容🥹"
                            )
                        )]
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
                            f"IG：@fan._.yuuu"
                        ))
                ]

        else:
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

    except Exception as e:
        return [
        TextSendMessage(text=f"❌ 發生錯誤了...\n📛 錯誤內容：{e}"),
        TextSendMessage(text="請檢查指令輸入格式！\n輸入 /help 查看可用指令 😎")
    ]