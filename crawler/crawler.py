import requests
from typing import Optional
from datetime import datetime

from crawler.stock import Stock

class TaiwanStockExchangeCrawler:
    BASE_URL: str = "https://www.twse.com.tw/exchangeReport/"
    
    REPORTS: dict[str, str] = {
        "每日收盤行情": "MI_INDEX",
        "三大法人買賣超": "T86",
        "個股每日歷史交易資料": "STOCK_DAY",
        "個股每日平均股價、成交量等": "STOCK_DAY_AVG"
    }

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
        }

    def fetch_raw_data(
        self, 
        report_name: str, 
        date: Optional[str] = None, 
        stock_no: Optional[str] = None,
        response_type: str = "json"
    ) -> dict:
        """
        根據指定的報表名稱、日期、股票代號，向台灣證券交易所（TWSE）取得 JSON 資料。

        參數：
            - report_name (str): 報表名稱，必須是以下其中一種：
                - "每日收盤行情"
                - "三大法人買賣超"
                - "個股每日歷史交易資料"
                - "個股每日平均股價、成交量等"
            - date (str, optional): 查詢日期，格式為 'YYYYMMDD'。
                若未提供，預設為今日。
            - stock_no (str, optional): 股票代號。
                僅當報表為「個股每日歷史交易資料」或「個股每日平均股價、成交量等」時需提供。
            - response_type (str): 回傳格式，預設為 "json"。其他格式可能為 "csv" 等（目前僅支援 json）。

        回傳：
            dict: 回傳的 JSON 資料。若回傳不是 JSON，將拋出 RuntimeError。
        
        例外處理：
            - ValueError: 若 report_name 無效。
            - RuntimeError: 若回傳格式非 JSON。
        """
        if report_name not in self.REPORTS:
            raise ValueError(f"找不到報表名稱：{report_name}")
        
        report_code = self.REPORTS[report_name]

        if not date:
            date = datetime.today().strftime("%Y%m%d")
        
        params = {
            "response": response_type,
            "date": date,
        }

        if report_code in ["STOCK_DAY", "STOCK_DAY_AVG"] and stock_no:
            params["stockNo"] = stock_no
        elif report_code == "T86":
            params["selectType"] = "ALLBUT0999"  # 除去0999的買賣超資料

        res = requests.get(f"{self.BASE_URL}{report_code}", params=params, headers=self.headers)
        try:
            return res.json()
        except ValueError:
            raise RuntimeError("回傳 API 沒資料或格式錯誤")

    def get_stock_by_no(self, stock_no: str,  date: Optional[str] = None) -> Stock:
        """
        從台灣證券交易所抓取指定股票的資料，並回傳一個 Stock 物件。
        """
        data = self.fetch_raw_data("個股每日歷史交易資料", date=date, stock_no=stock_no)
        return Stock(data)


if __name__ == "__main__":
    crawler = TaiwanStockExchangeCrawler()

    # 抓取 2024/04/12 的每日收盤行情
    data = crawler.fetch_raw_data("個股每日歷史交易資料", stock_no= "2330")
    print(data) 

    import json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
