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


def generate_plot_url(type: str, title: str, x_label: Optional[str], y_label: Optional[str], token: str):
    """
    產生圖表網址
    """
    return f"https://dobujio.onrender.com/plot?"\
        f"type={type}" \
        f"&title={urllib.parse.quote(title)}" \
        f"&x_label={urllib.parse.quote(x_label)}" \
        f"&y_label={urllib.parse.quote(y_label)}" \
        f"&token={urllib.parse.quote(token)}"