from typing import Optional

class Stock:
    """表示一檔股票及其每日成交資訊。"""
    
    def fields(self)-> dict[str, int]:
        return {field:index for index, field in enumerate(self.__raw_data.get("fields", []))}

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

        self.__raw_data = raw_data
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
    
    def get(self, field: str, date_range: Optional[tuple[str, str]] = None) -> list[str]:
        """
        取得指定欄位在指定日期的值，若未提供日期則取全部。

        參數:
            field (str): 欄位名稱。
            date_range (Optional[tuple[str, str]]): 查詢的日期區間 (起始日期, 結束日期)，格式為 '114/04/01'。若為 None，則回傳所有日期的資料。

        回傳:
            list[str]: 該欄位的資料列表 

        引發:
            KeyError: 欄位不存在。
        """
        if field not in self.fields():
            raise KeyError(f"無此欄位：{field}")
        if not self.__daily_data:
            return []
        index = self.fields()[field]

        if date_range:
            start, end = date_range
            return [row[index] for row in self.__daily_data if start <= row[0] <= end]
        else:
            return [row[index] for row in self.__daily_data]
        
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
