from linebot.models import SendMessage, TextSendMessage

def controller(_: str) -> list[SendMessage]:
    """
    處理 /test 指令，測試用
    """
    # 解析使用者輸入的文字，取得股票代號
    # 回覆訊息列表
    return [
            TextSendMessage(
                text="🧪 測試成功！\n測試都不揪喔❓😎"
            )
        ]