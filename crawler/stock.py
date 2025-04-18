from typing import Literal, Optional, Union

from .models import DAILY_DATA_JSON, DAILY_DATA_KEYS,  REAL_TIME_JSON, REAL_TIME_KEYS, real_time_fields

class Stock:
    """股票"""
    KEYS = Union[REAL_TIME_KEYS, Literal["每日交易資料"]]
    

    def __init__(self, stock_no: str=None):
        """
        建立 Stock 物件。

        參數:
            stock_no (str): 股票代號，若為 None 則不初始化資料。
        
        引發:
            ValueError: 若資料格式錯誤或缺少必要欄位。
        """
        if not stock_no:
            raise ValueError("無效的原始資料")

        self.__no = stock_no
        self.__data: dict[Stock.KEYS, str| list[dict[DAILY_DATA_KEYS, str]]] = {}
        
    def __str__(self) -> str:
        return f"{self.__no}: {self.get('股票簡稱')[0] or '無名稱'}"
    
    def set_data(self, daily_data: DAILY_DATA_JSON, real_time_data:REAL_TIME_JSON) -> None:
        """
        設定股票資料。

        參數:
            daily_data (DAILY_DATA_JSON): 每日交易資料，格式為 [日期, 開盤價, 最高價, 最低價, 收盤價, 成交股數, 成交金額]。
            real_time_data (REAL_TIME_JSON): 即時資料，格式為 {欄位名稱: 欄位值}。
        
        引發:
            ValueError: 若資料格式錯誤或缺少必要欄位。
        """
        if not daily_data or not real_time_data:
            raise ValueError("無效的原始資料")
    
        for key, symbol in real_time_fields.items():
            if symbol in real_time_data["msgArray"][0]:
                self.__data[key] = real_time_data["msgArray"][0][symbol]
                
        # 對每日資料進行結構化
        fields = daily_data["fields"]
        records = daily_data["data"]

        for row in records:
            day_data = {fields[i]: row[i] for i in range(len(fields))}
            self.__data.setdefault("每日交易資料", []).append(day_data)
            
    def get_data(self) -> dict[KEYS, str| list[dict[DAILY_DATA_KEYS, str]]]:
        return self.__data

    def get_no(self) -> str:
        return self.__no
    
    def get(self, key:KEYS, date_range: Optional[tuple[str, str]] = None) -> list[str|list[dict[DAILY_DATA_KEYS, str]]]:
        if key not in self.__data:
            raise KeyError(f"無此欄位：{key}")
        if not self.__data:
            return []
        
        if key == "每日交易資料":
            if date_range:
                start, end = date_range
                return [[data for data in self.__data["每日交易資料"] if start <= data["日期"] <= end]]
            return [self.__data["每日交易資料"]]
        
        return [self.__data[key]]
    
    
    def daily_field_transform(
        self,
        field: DAILY_DATA_KEYS,
        interval: Literal["day", "month"],
        date_range: Optional[tuple[str, str]] = None
    ) -> Optional[list[list[str,float]]]:
        """
        擷取每日交易資料中指定欄位的資料，並根據時間間隔進行聚合（每日或每月）。

        參數:
            field (DAILY_DATA_KEYS): 欲擷取的欄位，如 "收盤價"。
            interval (Literal["day", "month"]): 時間間隔，日或月。
            date_range (Optional[tuple[str, str]]): 起始與結束日期，格式為 YYYYMMDD。

        回傳:
        Optional[list[list[str,float]]] : 日期與對應的值的列表。
        """
        
        raw_data: list[dict[DAILY_DATA_KEYS, str]] = self.get("每日交易資料", date_range=date_range)[0]

        # 資料整理與轉換
        sorted_data: list[list[str, float]] = []
        for entry in raw_data:
            date = entry.get("日期")
            val_str = entry.get(field, "")
            try:
                val = float(val_str.replace(",", ""))
                sorted_data.append([date, val])
            except (ValueError, TypeError):
                continue

        if not sorted_data:
            return None

        # 資料排序
        sorted_data.sort(key=lambda x: x[0])

        # 聚合資料
        if interval == "month":
            monthly_data: dict[str, list[float]] = {}
            for date, value in sorted_data:
                yyyymm = date[:6]
                monthly_data.setdefault(yyyymm, []).append(value)
            return [[yyyymm, sum(values) / len(values)] for yyyymm, values in monthly_data.items()]
        else:
            return sorted_data

