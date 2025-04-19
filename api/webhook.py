import io
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, abort, request, send_file

import os
from dotenv import load_dotenv

import utils
from visualize import Chart
from .reply_handler import reply_handler

# 讀取 .env 環境變數
load_dotenv()

# 初始化 LINE Bot API 與 Webhook Handler
LINE_BOT = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
WEBHOOK = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)  # <-- Vercel 會自動找這個 app 當 handler

@app.route("/", methods=["GET"])
def index():
    return "The server is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
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
        reply_handler(event.message.text.strip())
    )

@app.route('/plot', methods=['GET'])
def plot():
    # 取得查詢參數
    type = request.args.get('type')
    match type:
        case "trend":
            title = request.args.get('title')
            x_label = request.args.get('x_label')
            y_label = request.args.get('y_label')
            token = request.args.get('token')
            data = utils.data.decompress_data(token)
            x_data = [d[0] for d in data]
            y_data = [d[1] for d in data]

            img_data = Chart.trend(
                title=title,
                x_label=x_label,
                y_label=y_label,
                x_data=x_data,
                y_data=y_data,
            )
        case "kline":
            title = request.args.get('title')
            token = request.args.get('token')
            data = utils.data.decompress_data(token)
            img_data = Chart.kline(
                title=title,
                data=data,
            )
        case "bar":
            title = request.args.get('title')
            x_label = request.args.get('x_label')
            y_label = request.args.get('y_label')
            token = request.args.get('token')
            data = utils.data.decompress_data(token)
            x_data = [d[0] for d in data]
            y_data = [d[1] for d in data]
            img_data = Chart.bar(
                title=title,
                x_label=x_label,
                y_label=y_label,
                x_data=x_data,
                y_data=y_data,
            )
        case _:
            return "不支援的圖表類型", 400
    
    if img_data is None:
        return "資料不足，無法繪圖", 400

    return send_file(
        io.BytesIO(img_data),
        mimetype='image/jpeg',
        as_attachment=False,
        download_name=f"{title}.jpg"
    )