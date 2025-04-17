from typing import Literal, TypedDict

DAILY_DATA_KEYS = Literal[
        "日期",
        "成交股數",
        "成交金額",
        "開盤價",
        "最高價",
        "最低價",
        "收盤價",
        "漲跌價差",
        "成交筆數",
    ]

class DAILY_DATA_JSON(TypedDict):
    stat: Literal["OK"] | str
    date: str  # 格式: "20250401"
    title: str
    fields: list[DAILY_DATA_KEYS]
    data: list[list[str]]
    notes: list[str]
    total: int


REAL_TIME_FIELDS = Literal[
    "@", "tv", "ps", "pid", "pz", "bp", "fv", "oa", "ob", "m%",
    "^", "key", "a", "b", "c", "#", "d", "%", "ch", "tlong",
    "ot", "f", "g", "ip", "mt", "ov", "h", "i", "it", "oz",
    "l", "n", "o", "p", "ex", "s", "t", "u", "v", "w",
    "nf", "y", "z", "ts"
]

REAL_TIME_KEYS = Literal[
    "股票代碼", "總委買筆數", "總委賣筆數", "相關股票", "前一日收盤價",
    "跌停價", "成交流水(千股)", "委買價", "委賣價", "暫無用途",
    "日期（西元年月日）", "資料鍵值（交易所_代碼_日期）", "五檔賣出價格（_分隔）",
    "五檔買入價格（_分隔）", "股票代碼（純數字）", "時間（最後更新時間）",
    "股票代碼（完整）", "時間戳（毫秒）", "最終撮合時間", "五檔買入量（_分隔）",
    "五檔賣出量（_分隔）", "總委買張數", "今日最高價", "最小跳動單位",
    "單位張數", "成交價（最後成交）", "今日最低價", "股票簡稱", "開盤價",
    "交易所", "成交筆數", "最後成交時間", "漲停價", "成交張數",
    "股票全名", "昨日收盤價", "目前成交價"
]

class QUERY_TIME(TypedDict):
    sysDate: str
    stockInfoItem: int
    stockInfo: int
    sessionStr: str
    sysTime: str
    showChart: bool
    sessionFromTime: int
    sessionLatestTime: int

class REAL_TIME_JSON(TypedDict):
    msgArray: list[dict[REAL_TIME_FIELDS, str]]
    referer: str
    userDelay: int
    rtcode: Literal["0000"]|str
    rtmessage: Literal["OK"]
    queryTime: QUERY_TIME
    exKey: str
    cachedAlive: int



real_time_fields: dict[REAL_TIME_KEYS, REAL_TIME_FIELDS]={
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