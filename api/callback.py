from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from flask import Flask, abort, request

import os
from dotenv import load_dotenv

# 讀取 .env 環境變數
load_dotenv()

# 初始化 LINE Bot API 與 Webhook Handler
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
webhook_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)  # <-- Vercel 會自動找這個 app 當 handler！

@app.route("/", methods=["GET"])
def index():
    return "The server is running!"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    
    print("Received signature:", signature)
    print("Request body:", body)

    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ Signature verification failed")
        abort(400)
    return "OK"

# 訊息事件處理：收到文字時自動回覆
@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event: MessageEvent):
    user_message = event.message.text
    reply_message = f"你說了：{user_message}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

