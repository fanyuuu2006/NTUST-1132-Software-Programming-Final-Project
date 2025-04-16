from datetime import datetime

class DateUtil:
    @staticmethod
    def roc_to_ad(roc: str, output_format: str = "%Y%m%d") -> str:
        """
        將民國日期字串（如 '114/04/15'）轉換為西元日期字串（如 '20250415'）。
        
        參數:
            roc (str): 民國日期字串，格式為 'YYY/MM/DD'。
            output_format (str): 輸出的日期格式（預設為 '%Y%m%d'）。
        
        回傳:
            str: 轉換後的西元日期字串。
        """
        try:
            y, m, d = map(int, roc.split('/'))
            return datetime(y+1911, m, d).strftime(output_format)
        except (ValueError, TypeError) as e:
            raise ValueError(f"無法轉換民國日期：{roc}，錯誤：{e}")
        
    @staticmethod
    def ad_to_roc(ad: str, fmt="%Y%m%d") -> str:
        """
        將西元日期字串（如 '20250415') 轉換為民國日期字串（如 '114/04/15'）。
        
        參數:
            ad (str): 西元日期字串，格式為 'YYYYMMDD'。
            fmt (str): 輸出的日期格式（預設為 '%Y%m%d'）。
        
        回傳:
            str: 轉換後的民國日期字串。
        """
        try:
            dt = datetime.strptime(ad, fmt)
            return f"{dt.year - 1911:03}/{dt.month:02}/{dt.day:02}"
        except (ValueError, TypeError) as e:
            raise ValueError(f"無法轉換西元日期：{ad}，錯誤：{e}")
        
    @staticmethod
    def month_range(start: str, end: str) -> list[str]:
        """
        從起訖日期（格式為 'YYYYMMDD'）產生每月第一天的字串清單。

        例如:
            start = '20210101', end = '20210315'
            回傳 = ['20210101', '20210201', '20210301']

        參數:
            start (str): 起始日期，格式為 'YYYYMMDD'。
            end (str): 結束日期，格式為 'YYYYMMDD'。

        回傳:
            list[str]: 每月第一天日期的字串清單。
        """
        try:
            start_dt = datetime.strptime(start, "%Y%m%d").replace(day=1)
            end_dt = datetime.strptime(end, "%Y%m%d").replace(day=1)

            result: set[str] = set()
            while start_dt <= end_dt:
                result.add(start_dt.strftime("%Y%m01"))                # 換下個月
                # 換到下個月
                if start_dt.month == 12:
                    start_dt = start_dt.replace(year=start_dt.year + 1, month=1)
                else:
                    start_dt = start_dt.replace(month=start_dt.month + 1)
                    
            return list(result)
        except (ValueError, TypeError) as e:
            raise ValueError(f"無法產生月份範圍：{start} ~ {end}，錯誤：{e}")
    
    
real_time_fields={
    "股票代碼": "@",
    "總委買筆數": "tv",
    "總委賣筆數": "ps",
    "相關股票": "pid",
    "前一日收盤價": "pz",
    "跌停價": "bp",
    "成交流水(千股)": "fv",
    "委買價": "oa",
    "委賣價": "ob",
    "暫無用途": "ts",
    "日期（西元年月日）": "d",
    "資料鍵值（交易所_代碼_日期）": "key",
    "五檔賣出價格（_分隔）": "a",
    "五檔買入價格（_分隔）": "b",
    "股票代碼（純數字）": "c",
    "時間（最後更新時間）": "%",
    "股票代碼（完整）": "ch",
    "時間戳（毫秒）": "tlong",
    "最終撮合時間": "ot",
    "五檔買入量（_分隔）": "f",
    "五檔賣出量（_分隔）": "g",
    "總委買張數": "ov",
    "今日最高價": "h",
    "最小跳動單位": "i",
    "單位張數": "it",
    "成交價（最後成交）": "oz",
    "今日最低價": "l",
    "股票簡稱": "n",
    "開盤價": "o",
    "交易所": "ex",
    "成交筆數": "s",
    "最後成交時間": "t",
    "漲停價": "u",
    "成交張數": "v",
    "股票全名": "nf",
    "昨日收盤價": "y",
    "目前成交價": "z"
}

