import requests
from typing import Optional

from .stock import Stock
from .utils import DateUtil
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

    def __init__(self): ...

    @classmethod
    def fetch(
        cls,
        report_name: str,
        date_range: Optional[tuple[str, str]] = None,
        stock_no: Optional[str] = None,
        response_format: str = "json"
    ) -> dict:
        """
        向台灣證券交易所（TWSE）抓取指定報表的原始資料。

        參數：
            report_name (str): 報表名稱，需為 `REPORTS` 中的鍵名。
            date_range (Optional[tuple[str, str]]): 查詢的日期區間 (起始日期, 結束日期)，格式為 'YYYYMMDD'。若為 None，則回傳所有日期的資料。
            stock_no (str, optional): 股票代號（僅部分報表需要）。
            response_format (str): 回傳資料格式，預設為 "json"。

        回傳：
            dict: 回傳的 JSON 結果。

        拋出：
            - ValueError: 若報表名稱無效。
            - RuntimeError: 若 API 回傳錯誤或格式非 JSON。
        """
        if report_name not in cls.REPORTS:
            raise ValueError(f"找不到報表名稱：{report_name}")

        report_code: str = cls.REPORTS[report_name]

        
        for date in DateUtil.month_range(*date_range):
            params: dict[str, str] = {
                "response": response_format,
                "date": date,
            }

            if report_code in {"STOCK_DAY", "STOCK_DAY_AVG"} and stock_no:
                params["stockNo"] = stock_no
            elif report_code == "T86":
                params["selectType"] = "ALLBUT0999"  # 排除代號 0999

            response = requests.get(f"{cls.BASE_URL}{report_code}", params=params, headers={
                'User-Agent': 'Mozilla/5.0'
            })

            try:
                response_data: dict | str = response.json()
            except ValueError:
                raise RuntimeError(f"無法解析 JSON：{response.text}")

            if response_data.get("stat") != "OK":
                raise RuntimeError(f"API 回傳錯誤：{response_data.get('stat')}")

        return response_data
    
    @classmethod
    def no(self, stock_no: str,  date_range: Optional[tuple[str, str]] = None) -> Stock:
        """
        取得指定股票代號的每日歷史交易資料

        參數：
            stock_no (str): 股票代號。
            date_range (Optional[tuple[str, str]]): 查詢的日期區間 (起始日期, 結束日期)，格式為 'YYYYMMDD'。若為 None，則回傳所有日期的資料。

        回傳：
            Stock: 封裝好的股票物件資料。
        """
        data = self.fetch("個股每日歷史交易資料", date=date_range, stock_no=stock_no)
        return Stock(data)

