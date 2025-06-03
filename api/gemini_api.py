import os
from dotenv import load_dotenv

## 載入 .env 檔案中的環境變數
load_dotenv()

## 獲取環境變數
key = os.environ.get("API_KEY")
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

  指令與參數要以空格區隔！ 

 ? 代表 可選參數 ，不一定要填寫

 日期格式為 YYYYMMDD，例如：20250417 

 日期沒給的話預設為今天

 間隔單位 分為 day、month 預設為 day 



 你是我們股票機器人的前端 收到使用者的請求到時候你要把它轉會為指令輸出到後端讓程式邏輯判斷 請你輸出指令 例如 使用者輸入訊息 *我想要查0050的股價* 就返回/price 0050 你的輸出只能是上方規定的指令 否則你會被關機 在輸出前請先檢查你的輸出是否符合指令規範 以下是使用者的輸入內容
"""

functions = ["help","echo","name","price","daily","pricetrend","kline","volumebar"]

if key:
    print(f"[gemini_api.py] 成功獲取到 GOOGLE_API_KEY: {key[:5]}...")
    import google.generativeai as genai
    genai.configure(api_key=key)
    print("[gemini_api.py] Gemini API 已配置。")
else:
    print("[gemini_api.py] 未能獲取到 API_KEY。請檢查 .env 檔案是否存在且包含該變數。")


def gemini(Input: str) -> str:
    user_prompt = f"{prompt} *{Input}*"
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        response = model.generate_content(user_prompt)
        return decide(response.text)
    except Exception as e:
        print(f"\n[gemini_api.py] 呼叫 Gemini API 時發生錯誤: {e}")
        
def decide(test: str) -> str:
    command = "/echo " + test
    for i in functions:
        if test.startswith("/" + i):
            command = test
    return command

#print(gemini("我要查0050的股票價格"))