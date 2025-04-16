from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from flask import Flask, abort, request

import os
from dotenv import load_dotenv

from .text_handler import text_handler

# 讀取 .env 環境變數
load_dotenv()

# 初始化 LINE Bot API 與 Webhook Handler
LINE_BOT = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
WEBHOOK = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)  # <-- Vercel 會自動找這個 app 當 handler

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
        WEBHOOK.handle(body, signature)
    except InvalidSignatureError:
        print("❌ Signature verification failed")
        abort(400)
    return "OK"

# 處理文字訊息事件
@WEBHOOK.add(MessageEvent, message=TextMessage)
def handle_text_message(event: MessageEvent):
    LINE_BOT.reply_message(
        event.reply_token,
        text_handler(event.message.text)
    )

