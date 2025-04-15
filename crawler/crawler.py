import requests
from typing import Optional
from datetime import datetime

from .stock import Stock

class TaiwanStockExchangeCrawler:
    """
    台灣證券交易所資料爬蟲，用來抓取特定報表的每日交易資訊。
    """
    
    BASE_URL: str = "https://www.twse.com.tw/exchangeReport/"
    
    REPORTS: dict[str, str] = {
        "每日收盤行情": "MI_INDEX",
        "三大法人買賣超": "T86",
        "個股每日歷史交易資料": "STOCK_DAY",
        "個股每日平均股價、成交量等": "STOCK_DAY_AVG"
    }

    def __init__(self):
        """初始化 crawler 並設定 headers。"""
        self.headers: dict[str, str] = {
            'User-Agent': 'Mozilla/5.0'
        }

    def fetch_raw_data(
        self,
        report_name: str,
        date: Optional[str] = None,
        stock_no: Optional[str] = None,
        response_format: str = "json"
    ) -> dict:
        """
        向台灣證券交易所（TWSE）抓取指定報表的原始資料。

        參數：
            report_name (str): 報表名稱，需為 `REPORTS` 中的鍵名。
            date (str, optional): 查詢日期（格式：YYYYMMDD）。預設為今日。
            stock_no (str, optional): 股票代號（僅部分報表需要）。
            response_format (str): 回傳資料格式，預設為 "json"。

        回傳：
            dict: 回傳的 JSON 結果。

        拋出：
            - ValueError: 若報表名稱無效。
            - RuntimeError: 若 API 回傳錯誤或格式非 JSON。
        """
        if report_name not in self.REPORTS:
            raise ValueError(f"找不到報表名稱：{report_name}")

        report_code: str = self.REPORTS[report_name]
        query_date: str = date or datetime.today().strftime("%Y%m%d")

        params: dict[str, str] = {
            "response": response_format,
            "date": query_date,
        }

        if report_code in {"STOCK_DAY", "STOCK_DAY_AVG"} and stock_no:
            params["stockNo"] = stock_no
        elif report_code == "T86":
            params["selectType"] = "ALLBUT0999"  # 排除代號 0999

        response = requests.get(f"{self.BASE_URL}{report_code}", params=params, headers=self.headers)

        try:
            response_data = response.json()
        except ValueError:
            raise RuntimeError(f"無法解析 JSON：{response.text}")

        if response_data.get("stat") != "OK":
            raise RuntimeError(f"API 回傳錯誤：{response_data.get('stat')}")

        return response_data

    def get_stock_by_no(self, stock_no: str,  date: Optional[str] = None) -> Stock:
        """
        取得指定股票的每日歷史交易資料，回傳 Stock 物件。

        參數：
            stock_no (str): 股票代號。
            date (str, optional): 查詢日期（格式：YYYYMMDD），預設為今日。

        回傳：
            Stock: 封裝好的股票物件資料。
        """
        data = self.fetch_raw_data("個股每日歷史交易資料", date=date, stock_no=stock_no)
        return Stock(data)


if __name__ == "__main__":
    crawler = TaiwanStockExchangeCrawler()

    s = crawler.get_stock_by_no("2330").get_all_by_field("日期")
    print(s)
