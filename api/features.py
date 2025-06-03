from linebot.models import (
    SendMessage,
    TextSendMessage,
)

from typing import Callable, Literal

from .controllers import name, price, daily, kline, volumebar, pricetrend


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
    "/echo": {
        "description": "回傳你輸入的訊息內容（測試用）",
        "format": "/echo <訊息>",
        "controller": lambda text: [
        TextSendMessage(
            text= text.partition(" ")[2] + "都不揪❓"
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