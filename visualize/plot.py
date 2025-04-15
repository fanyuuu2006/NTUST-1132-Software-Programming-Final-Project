from typing import Optional
import matplotlib.pyplot as plt
from matplotlib import rcParams

from crawler import Stock

# 設定字型為 Windows 系統內建字型
rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
rcParams['axes.unicode_minus'] = False  # 確保負號能顯示

def plot_stock_trend(stock: Stock, field: str = "收盤價", date_range: Optional[tuple[str, str]] = None) -> None:
    """
    繪製股票指定欄位的時間趨勢圖。

    參數:
        stock (Stock): Stock 物件
        field (str): 欲繪製的欄位名稱（預設為「收盤價」）
        date_range (Optional[tuple[str, str]]): 查詢的日期區間 (起始日期, 結束日期)，格式為 '114/04/01'。若為 None，則回傳所有日期的資料。
    """
    
    dates = stock.get("日期", date_range)
    values = stock.get(field, date_range)

    # 將「收盤價」等轉為 float，並忽略無法轉換的項目（如 "--"）
    cleaned_dates = []
    cleaned_values = []
    for date, val in zip(dates, values):
        try:
            cleaned_values.append(float(val.replace(",", "")))
            cleaned_dates.append(date)
        except ValueError:
            continue

    if not cleaned_values:
        print("沒有可用資料繪圖")
        return

    plt.plot(cleaned_dates, cleaned_values, marker='o', linestyle='-', color='blue')
    plt.xticks(rotation=45) # 把 x 軸的文字（日期）旋轉 45 度，避免太擠重疊。
    plt.title(f"{stock.get_no()} {stock.get_name()} - {field} 趨勢圖")
    plt.xlabel("日期")
    plt.ylabel(field)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    