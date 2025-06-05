from typing import Optional
import requests
import urllib.parse

def shorten_url(url: str) -> str:
    """
    使用 TinyURL API 縮短網址。
    
    參數：
        url (str): 要縮短的網址。    
    回傳：
        str: 縮短後的網址。
    """
    
    response = requests.get("https://tinyurl.com/api-create.php", params={"url": url})
    return response.text  # 短網址



def generate_plot_url(
    type: str,
    title: str,
    token: str,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
) -> str:
    """
    根據提供的圖表資訊產生 URL，該網址可用於請求遠端圖表圖片。

    參數:
        type (str): 圖表類型（如 "trend", "bar", "kline" 等）。
        title (str): 圖表標題。
        x_label (Optional[str]): X 軸標籤，若為 None 則省略。
        y_label (Optional[str]): Y 軸標籤，若為 None 則省略。
        token (str): 身分驗證或資料辨識用的 Token。

    回傳:
        str: 已編碼的完整圖表請求網址。
    """
    params = {
        "type": type,
        "title": title,
        "token": token
    }
    if x_label is not None:
        params["x_label"] = x_label
    if y_label is not None:
        params["y_label"] = y_label

    query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    return f"https://dobujio.onrender.com/plot?{query_string}"