from typing import Optional

class Stock:
    """表示一檔股票及其每日成交資訊。"""
    
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
        """
        建立 Stock 物件。

        參數:
            raw_data (dict): 包含 'title' 和 'data' 的原始資料。
        
        引發:
            ValueError: 若資料格式錯誤或缺少必要欄位。
        """
        if not raw_data or "data" not in raw_data or "title" not in raw_data:
            raise ValueError("無效的原始資料")

        self.raw_data = raw_data
        self.__no, self.__name = self.extract_info(raw_data["title"])
        self.__daily_data: list[list[str]] = raw_data["data"]

    def __str__(self) -> str:
        return f"{self.__no}: {self.__name}（{len(self.__daily_data)} 筆資料）"

    def get_name(self) -> str:
        return self.__name

    def get_no(self) -> str:
        return self.__no

    def get_daily_data(self) -> list[list[str]]:
        """
        取得原始每日資料。

        回傳:
            list[list[str]]: 每日資料的二維清單。
        """
        return self.__daily_data
    
    def get_all_by_field(self, field: str) -> list[str]:
        """
        取得指定欄位的所有資料。

        參數:
            field (str): 欲查詢的欄位名稱（如 "收盤價"）。

        回傳:
            list[str]: 指定欄位的所有值。

        引發:
            KeyError: 欄位不存在。
        """
        if field not in Stock.FIELDS:
            raise KeyError(f"無此欄位：{field}")
        index = Stock.FIELDS[field]
        return [ row[index] for row in self.__daily_data]

    def get_field_by_date(self, field: str, date: Optional[str] = None) -> Optional[str]:
        """
        取得指定欄位在指定日期的值，若未提供日期則取最新一筆。

        參數:
            field (str): 欄位名稱。
            date (str, optional): 查詢的日期（格式：'114/04/15'），預設為最新一筆。

        回傳:
            Optional[str]: 欄位資料，或 None（若資料不存在）。

        引發:
            KeyError: 欄位不存在。
        """
        if field not in Stock.FIELDS:
            raise KeyError(f"無此欄位：{field}")
        if not self.__daily_data:
            return None
        index = Stock.FIELDS[field]

        if date:
            for row in self.__daily_data:
                if row[Stock.FIELDS["日期"]] == date:
                    return row[index]
            return None  # 沒有找到該日期
        else:
            return self.__daily_data[-1][index]

    @staticmethod
    def extract_info(title: str) -> tuple[str, str]:
        """
        從標題字串中擷取股票代號與名稱。

        範例標題："114年04月 2330 台積電 各日成交資訊"

        參數:
            title (str): 標題字串。

        回傳:
            tuple[str, str]: (股票代號, 股票名稱)。

        引發:
            ValueError: 若標題格式錯誤。
        """
        parts = title.split()
        if len(parts) < 3:
            raise ValueError("標題格式錯誤，無法解析股票代號與名稱")
        stock_no = parts[1]
        stock_name = parts[2]
        return stock_no, stock_name
