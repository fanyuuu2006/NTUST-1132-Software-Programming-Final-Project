import json
from typing import Callable, Literal
from crawler import TaiwanStockExchangeCrawler

features: dict[str, dict[Literal["keyword", "handler"], list[str]]|Callable[[str], str]] = {
    "根據代號查詢股票":{
        "keyword": ["查","查詢股票", "查詢", "查股票", "代號", "股票代號"],
        "handler": lambda text: TaiwanStockExchangeCrawler.no(text).get_name()
    }
}

def text_handler(text: str)-> list[str]: 
    """
    根據傳入的文字，取得對應的回覆內容。
    """
    
    for feature, data in features.items():
        if any(keyword in text for keyword in data["keyword"]):
            return [data["handler"](text)]
    
    with open("json/dialoglib.json", "r", encoding="utf-8") as f:
        dialoglib: dict = json.load(f)
        return [dialoglib[text] if text in dialoglib else "玩股票都不揪喔❓你今天想幹嘛呢\n😎"]
    
    
