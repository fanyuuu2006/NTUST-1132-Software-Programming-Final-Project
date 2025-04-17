import io
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from flask import Flask, abort, request, send_file

import os
from dotenv import load_dotenv

from crawler import TaiwanStockExchangeCrawler
from visualize import trend

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

@app.route('/plot/<stock_no>', methods=['GET'])
def plot(stock_no):
    # 取得查詢參數
    if "field" not in request.args:
        return "請提供查詢的欄位", 400
    if "interval" not in request.args:
        return "請提供查詢的時間間隔", 400
    
    field = request.args.get('field')
    interval = request.args.get('interval')
    start = request.args.get('start')
    end = request.args.get('end')

    # 組合日期範圍（可為 None）
    date_range = (start, end) if start and end else None

    img_data = trend(TaiwanStockExchangeCrawler.no(stock_no, date_range), field=field, date_range=date_range, interval=interval)

    if img_data is None:
        return "資料不足，無法繪圖", 400

    return send_file(
        io.BytesIO(img_data),
        mimetype='image/jpeg',
        as_attachment=False,
        download_name=f"{stock_no}_{field}.jpg"
    )