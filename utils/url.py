import requests

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


