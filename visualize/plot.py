from io import BytesIO
from typing import Literal, Optional
import matplotlib.pyplot as plt
from matplotlib import rcParams, font_manager

from crawler import Stock
from crawler.models import DAILY_DATA_KEYS

# 設定字型使用跨平台中文字型
prop = font_manager.FontProperties(fname="assets/fonts/NotoSansTC-Regular.ttf")
rcParams['font.sans-serif'] = ['Noto Sans CJK TC']
rcParams['axes.unicode_minus'] = False  # 確保負號能顯示


def trend(
    stock: Stock,
    field: DAILY_DATA_KEYS,
    date_range: Optional[tuple[str, str]] = None,
    interval: Literal["day", "month"] = "day"
) -> Optional[bytes]:
    """
    生成指定股票的趨勢圖並返回圖表的二進位資料。
    
    參數:
    stock (Stock): 需要繪製趨勢圖的股票物件。
    field (DAILY_DATA_KEYS): 股票資料的欄位（例如：開盤價、收盤價等）。
    date_range (tuple[str, str], optional): 需要顯示的日期範圍，格式為 ('YYYYMMDD', 'YYYYMMDD')，預設為 None。
    interval (Literal["day", "month"]): 設定為 "day" 時顯示日間資料，"month" 時顯示月統計平均值，預設為 "day"。

    回傳:
    Optional[bytes]: 返回趨勢圖的 JPEG 格式二進位資料，若資料不完整則返回 None。
    """

    dates = [data["日期"] for data in stock.get(key="每日交易資料", date_range=date_range)[0]]
    values = [data[field] for data in stock.get(key="每日交易資料", date_range=date_range)[0]]

    # 清理資料
    cleaned_dates: list[str] = []
    cleaned_values: list[float] = []
    for date, val in zip(dates, values):
        try:
            cleaned_values.append(float(val.replace(",", "")))
            cleaned_dates.append(date)
        except ValueError:
            continue

    if not cleaned_values:
        print("沒有可用資料繪圖")
        return None
    
    # 月統計平均
    if interval == "month":
        month_data: dict[str, list[float]] = {}
        for date_str, value in sorted(zip(cleaned_dates, cleaned_values)):
            yyyymm = date_str[:6] # 取出年份與月份
            month_data.setdefault(yyyymm, []).append(value)
        cleaned_dates = list(month_data.keys())
        cleaned_values = [sum(vals) / len(vals) for vals in month_data.values()]

    # 開始畫圖
    fig, ax = plt.subplots()
    for i in range(1, len(cleaned_dates)):
        prev_val, curr_val = cleaned_values[i - 1], cleaned_values[i]
        prev_date, curr_date = cleaned_dates[i - 1], cleaned_dates[i]
        color = 'red' if curr_val >= prev_val else 'green'
        ax.plot(
            [prev_date, curr_date],
            [prev_val, curr_val],
            color=color,
            marker='o',
            linestyle='-'
        )

    ax.set_xticks(range(len(cleaned_dates)))
    ax.set_xticklabels(cleaned_dates , rotation=45, ha='right')

    # 標題與格式
    ax.set_title(f"{stock.get_no()} {stock.get('股票簡稱')} - {field} 趨勢圖")
    ax.set_xlabel("日期")
    ax.set_ylabel(field)
    ax.grid(True)
    
    # 自動調整圖表佈局，避免標籤擁擠
    fig.tight_layout()

    # 儲存圖表為 bytes
    buf = BytesIO()
    fig.savefig(buf, format='jpeg')
    plt.close(fig)
    buf.seek(0)
    return buf.read()
