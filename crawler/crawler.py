from datetime import datetime
import time
import requests
from typing import Literal, Optional

from .stock import Stock
from .utils import DateUtil
class TaiwanStockExchangeCrawler:
    """
    台灣證券交易所資料爬蟲
    """
    URL_KEYS = Literal[
        "交易報表",
        "即時資訊"
    ]
    URLS: dict[URL_KEYS,str] = {
        "交易報表":"https://www.twse.com.tw/exchangeReport",
        "即時資訊":"https://mis.twse.com.tw/stock/api/getStockInfo.jsp", 
        }
        
    REPORTS_KEYS=Literal[
        "每日收盤行情",
        "三大法人買賣超",
        "個股每日歷史交易資料",
        "個股每日平均股價、成交量等",
        "融資融券與借券成交明細",
        "法人持股統計",
        
    ]
    REPORTS: dict[REPORTS_KEYS, str] = {
        "每日收盤行情": "MI_INDEX",
        "三大法人買賣超": "T86",
        "個股每日歷史交易資料": "STOCK_DAY",
        "個股每日平均股價、成交量等": "STOCK_DAY_AVG",
        "融資融券與借券成交明細": "MI_MARGN", 
        "法人持股統計": "MI_INDEX20",             
    }

    def __init__(self): ...

    @classmethod
    def fetch(cls, url: str, params: dict) -> dict:
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
        except ValueError:
            raise RuntimeError(f"無法解析 JSON：{response.text}")
        except requests.RequestException as e:
            raise RuntimeError(f"請求失敗：{e}")
        
        if "stat" not in data and 'rtmessage' not in data:
            raise RuntimeError("API 回傳格式錯誤，無法解析")

        for key in ["stat", "rtmessage"]:
            if key in data and data[key] != "OK":
                raise RuntimeError(f"API 回傳錯誤：[{key}: {data[key]}]")

        return data

    @classmethod
    def report(
        cls,
        report_name: REPORTS_KEYS,
        date_range: Optional[tuple[str, str]] = None,
        stock_no: Optional[str] = None,
        response_format: str = "json"
    ) -> dict:
        """
        向台灣證券交易所（TWSE）抓取指定報表的原始資料。

        參數：
            report_name (str): 報表名稱，需為 `REPORTS` 中的鍵名。
            date_range (Optional[tuple[str, str]]): 查詢的日期區間 (起始日期, 結束日期)，格式為 'YYYYMMDD'。若為 None，則回傳本月的資料。
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
        
        if date_range is None:
            today = datetime.today().strftime("%Y%m%d")
            date_range = (today, today)  # 預設為今天的日期範圍

        report_code: str = cls.REPORTS[report_name]

        result: dict = {}
        
        for date in DateUtil.month_range(*date_range):
            params: dict[str, str] = {
                "response": response_format,
                "date": date,
            }
            
            match report_code:
                case "STOCK_DAY" | "STOCK_DAY_AVG":
                    params["stockNo"] = stock_no
                case "MI_MARGN":
                    params["selectType"] = "margin"  # 範例，實際可查 twse 參數
                case "T86":
                    params["selectType"] = "ALLBUT0999"  # 排除代號 0999
                    
            data = cls.fetch(f"{cls.URLS["交易報表"]}/{report_code}", params)
            # 將民國日期轉換西元
            try:
                date_index = data["fields"].index("日期")
            except ValueError:
                date_index = None  # 若沒有日期欄位就略過轉換

            if date_index is not None:
                for row in data.get("data", []):
                    try:
                        row[date_index] = DateUtil.roc_to_ad(row[date_index], output_format="%Y%m%d")
                    except Exception:
                        pass  # 無法轉換的就略過
            
            if not result:
                result = data
            else:
                result["data"].extend(data.get("data", []))  # 合併每月資料
            time.sleep(0.1) # 等待 0.1 秒，避免 API 被鎖
        return result

    @classmethod
    def real_time(cls, stock_no: str) -> dict:
        """
        取得指定股票代號即時資料

        參數：
            stock_no (str): 股票代號。

        回傳：
            dict: 即時資料。
        """
        return cls.fetch(cls.URLS["即時資訊"], {"ex_ch": f"tse_{stock_no}.tw"})
    
    @classmethod
    def no(cls, stock_no: str,  date_range: Optional[tuple[str, str]] = None) -> Stock:
        """
        取得指定股票代號的每日歷史交易資料

        參數：
            stock_no (str): 股票代號。
            date_range (Optional[tuple[str, str]]): 查詢的日期區間 (起始日期, 結束日期)，格式為 'YYYYMMDD'。若為 None，則回傳所有日期的資料。

        回傳：
            Stock: 封裝好的股票物件資料。
        """
        stock = Stock(stock_no)
        stock.set_data(
            daily_data= cls.report("個股每日歷史交易資料", date_range, stock_no),
            real_time_data=cls.real_time(stock_no)
        )
        return stock