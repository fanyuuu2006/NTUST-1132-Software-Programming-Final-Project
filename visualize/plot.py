from io import BytesIO
from typing import Literal, Optional
import matplotlib.pyplot as plt
from matplotlib import rcParams, font_manager

from crawler import Stock
from crawler.models import DAILY_DATA_KEYS

# 設定中文字型與負號顯示
prop = font_manager.FontProperties(fname="assets/fonts/NotoSansTC-Regular.ttf")
rcParams['axes.unicode_minus'] = False

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
    raw_data:list[dict[DAILY_DATA_KEYS, str]] = stock.get(key="每日交易資料", date_range=date_range)[0]

    # 資料整理與轉換
    parsed_data: list[tuple[str, float]] = []
    for entry in raw_data:
        date = entry["日期"]
        val_str = entry.get(field, "")
        try:
            val = float(val_str.replace(",", ""))
            parsed_data.append((date, val))
        except (ValueError, TypeError):
            continue

    if not parsed_data:
        print("沒有可用資料繪圖")
        return None

    # 資料排序
    parsed_data.sort(key=lambda x: x[0])  # 日期排序，預設為字串比較

    # 若為月統計，轉換為月平均
    if interval == "month":
        monthly_data: dict[str, list[float]] = {}
        for date, value in parsed_data:
            yyyymm = date[:6]
            monthly_data.setdefault(yyyymm, []).append(value)
        cleaned_dates = list(monthly_data.keys())
        cleaned_values = [sum(vals) / len(vals) for vals in monthly_data.values()]
    else:
        cleaned_dates, cleaned_values = zip(*parsed_data)

    # 畫圖
    fig, ax = plt.subplots(figsize=(max(8, len(cleaned_dates) * 0.3), 5))
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
    ax.set_xticklabels(cleaned_dates, rotation=60, ha='right', fontproperties=prop)

    ax.set_title(f"{stock.get_no()} {stock.get('股票簡稱')} - {field} 趨勢圖", fontproperties=prop)
    ax.set_xlabel("日期", fontproperties=prop)
    ax.set_ylabel(field, fontproperties=prop)
    ax.grid(True)

    fig.tight_layout()

    # 圖轉為 bytes
    buf = BytesIO()
    fig.savefig(buf, format='jpeg')
    plt.close(fig)
    buf.seek(0)
    return buf.read()
