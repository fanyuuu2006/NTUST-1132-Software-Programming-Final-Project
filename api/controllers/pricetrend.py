from linebot.models import SendMessage, ImageSendMessage, TextSendMessage

import utils
def controller(text: str) -> list[SendMessage]:
    """
    處理 /pricetrend 指令，獲取期間內收盤價走勢圖
    """
    # 解析使用者輸入的文字，取得股票代號
    part = text.split(" ")
    stock_no = part[1]
    start_date = part[2] if len(part) > 2 else utils.date.today().replace(day=1)
    end_date = part[3] if len(part) > 3 else utils.date.today()
    interval = part[4] if len(part) > 4 else "day"

    url = f'https://dobujio.vercel.app/plot/{stock_no}?field=收盤價&start={start_date}&end={end_date}&interval={interval}'
    # 回覆訊息列表
    return [
            TextSendMessage(
                text=url
            ),
            ImageSendMessage(
                    original_content_url=url,
                    preview_image_url=url
                )
            ]