from typing import Optional

class Stock:
    """股票"""

    FIELDS: dict[str, int] = {
        "日期": 0,
        "成交股數": 1,
        "成交金額": 2,
        "開盤價": 3,
        "最高價": 4,
        "最低價": 5,
        "收盤價": 6,
        "漲跌價差": 7,
        "成交筆數": 8
    }

    def __init__(self, raw_data: dict):
        if not raw_data or "data" not in raw_data or "title" not in raw_data:
            raise ValueError("無效的原始資料")

        self.raw_data = raw_data
        self.__no, self.__name = self.extract_info(raw_data["title"])
        self.__data: list[list[str]] = raw_data["data"]

    def __str__(self) -> str:
        return f"{self.__no}: {self.__name}（{len(self.__data)} 筆資料）"

    def get_name(self) -> str:
        return self.__name

    def get_no(self) -> str:
        return self.__no

    def get_data(self) -> list[list[str]]:
        return self.__data

    def get_field(self, field: str) -> list[str]:
        if field not in self.FIELDS:
            raise KeyError(f"無此欄位：{field}")
        index = self.FIELDS[field]
        return [row[index] for row in self.__data]

    def get_latest_price(self) -> Optional[float]:
        if not self.__data:
            return None
        latest_row = self.__data[-1]
        price_str = latest_row[self.FIELDS["收盤價"]].replace(",", "").strip()
        try:
            return float(price_str)
        except ValueError:
            return None

    @staticmethod
    def extract_info(title: str) -> tuple[str, str]:
        """
        從標題字串中擷取股票代號與名稱。
        例如： "114年04月 2330 台積電 各日成交資訊"
        
        回傳：
           tuple[str, str]: (股票代號, 股票名稱)。
        """
        parts = title.split()
        if len(parts) < 3:
            raise ValueError("標題格式錯誤，無法解析股票代號與名稱")
        stock_no = parts[1]
        stock_name = parts[2]
        return stock_no, stock_name
