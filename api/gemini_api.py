import os
from dotenv import load_dotenv
import google.generativeai as genai
from .features import features

## 載入 .env 檔案中的環境變數
load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = """
 /echo <訊息> 

 查詢股票名稱 

 /name <股票代號> 

 查詢即時股價 

 /price <股票代號> 

 查詢期間內每日交易資訊 

 /daily <股票代號> <起始日期?> <結束日期?> 

 獲取期間內指定股票之收盤價趨勢圖 

 /pricetrend <股票代號> <起始日期?> <結束日期?> <間隔單位?> 

 獲取期間內指定股票之K線圖 

 /kline <股票代號> <起始日期?> <結束日期?> 

 獲取期間內指定股票之成交量長條圖 

 /volumebar <股票代號> <起始日期?> <結束日期?> <間隔單位?> 

指令與各個參數要以空格區隔！ 

 ? 代表 可選參數 ，不一定要填寫

 日期格式為 YYYYMMDD，例如：20250417 

 日期沒給的話預設為今天

 間隔單位 分為 day、month 預設為 day 



 你是我們股票機器人的前端 收到使用者的請求到時候你要把它轉會為指令輸出到後端讓程式邏輯判斷 請你輸出指令 例如 使用者輸入訊息 *我想要查0050的股價* 就返回/price 0050 *我想要看台積電上個月的K線圖* 就返回/kline 2330 `20250401` `20250430` (假設今天是2025年5月) 你的輸出只能是上方規定的指令 否則你會被關機 在輸出前請先檢查你的輸出是否符合指令規範 以下是使用者的輸入內容
"""

def decide(test: str) -> str:
    for i in features.keys():
        if test.startswith(i):
            return test
    return "/echo " + test

def gemini(input_message: str) -> str:
    user_prompt = f"{prompt} *{input_message}*"
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        response = model.generate_content(user_prompt)
        return decide(response.text)
    except Exception as e:
        raise RuntimeError(f"\n[gemini_api.py] 呼叫 Gemini API 時發生錯誤: {e}")
