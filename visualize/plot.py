from io import BytesIO
from typing import Literal, Optional
import matplotlib.pyplot as plt
from matplotlib import rcParams

from crawler import Stock

# 設定字型為 Windows 系統內建字型
rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
rcParams['axes.unicode_minus'] = False  # 確保負號能顯示


def plot_stock_trend(
    stock: Stock,
    field: str = "收盤價",
    date_range: Optional[tuple[str, str]] = None,
    interval: Literal["day", "month"] = "day"
) -> bytes:

    """
    根據傳入的 Stock 物件，繪製指定欄位的股票價格趨勢圖，
    並以 PNG 圖片格式回傳圖表的二進位資料，適合用於 API 回傳圖片。

    參數:
        stock (Stock): Stock 類別的實例，包含股票的歷史資料。
        field (str): 欲繪製的資料欄位名稱（預設為 "收盤價"），例如「開盤價」、「最高價」、「成交量」等。
        date_range (Optional[tuple[str, str]]): 日期範圍，格式為民國年月日，例如 ('114/04/01', '114/04/15')。若為 None 則使用全區間。
        interval (Literal["day", "month"]): 時間間隔方式：
            - "day": 每日資料
            - "month": 每月資料取平均值

    回傳:
        bytes: 繪製完成的 PNG 圖片的二進位資料，可用於網頁或 API 圖片輸出。
               若資料不足（無法繪圖）則回傳 None。

    注意事項:
        - 若資料中出現無法轉換為數字的值（如 "--"），會自動略過。
        - 輸出結果可透過 Web 框架（如 Flask、FastAPI）以 `image/jpeg` MIME 類型回傳。
    """
    
    dates = stock.get("日期", date_range)
    values = stock.get(field, date_range)

    # 將「收盤價」等轉為 float，並忽略無法轉換的項目（如 "--"）
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
        return
    
     # 若為「month」模式，彙總每月平均
    if interval == "month":
        month_data: dict[str,list[float]] = {}

        for date_str, value in sorted(zip(cleaned_dates, cleaned_values)):
            year, month= date_str[:4], date_str[4:6] # 取得年月 YYYYMM
            month_key = f"{year}/{month}"
            month_data.setdefault(month_key, []).append(value) 
        cleaned_dates = list(month_data.keys())
        cleaned_values = [sum(vals)/len(vals) for vals in month_data.values()]

    plt.plot(cleaned_dates, cleaned_values, marker='o', linestyle='-', color='blue')
    plt.xticks(rotation=45) # 把 x 軸的文字（日期）旋轉 45 度，避免太擠重疊。
    plt.title(f"{stock.get_no()} {stock.get_name()} - {field} 趨勢圖")
    plt.xlabel("日期")
    plt.ylabel(field)
    plt.grid(True)
    plt.tight_layout()
    buf = BytesIO() # 建立記憶體緩衝區
    plt.savefig(buf, format='jpeg') # 儲存圖片到緩衝區
    plt.close()
    buf.seek(0) # 移回緩衝區開頭
    return buf.read()

    