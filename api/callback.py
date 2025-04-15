from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from flask import Request, abort

import os
from dotenv import load_dotenv

# 讀取 .env 環境變數
load_dotenv()

# 初始化 LINE Bot API 與 Webhook Handler
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
webhook_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 定義 webhook callback handler（Vercel 會呼叫此函數）
# Vercel 會尋找名為 `handler` 的變數作為進入點
def handler(request: Request):
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    # 驗證來自 LINE 的請求，避免被偽造。
    try:
        webhook_handler.handle(body, signature)  # 驗證成功後會觸發事件分派
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 訊息事件處理：收到文字時自動回覆
@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event: MessageEvent):
    user_message = event.message.text
    reply_message = f"你說了：{user_message}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

