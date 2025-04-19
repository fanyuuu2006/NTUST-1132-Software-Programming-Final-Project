from io import BytesIO
from typing import Optional
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager


matplotlib.use('Agg')

# 設定中文字型與負號顯示
font_path = "assets/fonts/NotoSansTC-Regular.ttf"
font_prop = font_manager.FontProperties(fname=font_path)


def trend(
    title: str,
    x_label: str,
    y_label: str,
    x_data: list[str],
    y_data: list[float|int],
) -> Optional[bytes]:
    """
    根據提供的資料繪製折線圖，並依照漲跌變化以紅綠線段標示，輸出為 JPEG 圖片的位元資料。

    參數:
        title (str): 圖表標題。
        x_label (str): Y 軸標籤（注意：參數名是 x_label，但實際作用於 Y 軸）。
        y_label (str): X 軸標籤（注意：參數名是 y_label，但實際作用於 X 軸）。
        x_data (list[str]): 橫軸資料，通常為日期。
        y_data (list[float | int]): 縱軸資料，通常為數值，如股價或交易量。

    回傳:
        Optional[bytes]: 圖片的位元資料（JPEG 格式），可供儲存或回傳至前端。若資料無效則回傳 None。
    """
    if not x_data or not y_data or len(x_data) != len(y_data):
        return None

    # 畫圖
    fig, ax = plt.subplots(figsize=(max(8, len(x_data) * 0.3), 5))
    # 建立漲跌分組
    up_segments: list[tuple[list[float|int]]] = []
    down_segments: list[tuple[list[float|int]]] = []

    x_indices = list(range(len(x_data))) # 讓 matplotlib 使用數字索引來表示 x 軸的位置

    for i in range(1, len(x_data)):
        segment = ([x_indices[i - 1], x_indices[i]], [y_data[i - 1], y_data[i]]) 
        if y_data[i] >= y_data[i - 1]:
            up_segments.append(segment)
        else:
            down_segments.append(segment)

    # 畫紅色上漲線段
    for x, y in up_segments:
        ax.plot(x, y, color='red', marker='o', linestyle='-')

    # 畫綠色下跌線段
    for x, y in down_segments:
        ax.plot(x, y, color='green', marker='o', linestyle='-')


    ax.set_xticks(range(len(x_data)))
    ax.set_xlim(-0.5, len(x_data) - 0.5)
    ax.set_xticklabels(x_data, rotation=60, ha='right', fontproperties=font_prop)

    ax.set_title(title, fontproperties=font_prop)
    ax.set_xlabel(y_label, fontproperties=font_prop)
    ax.set_ylabel(x_label, fontproperties=font_prop)
    ax.grid(True)

    fig.tight_layout()

    # 圖轉為 bytes
    buf = BytesIO()
    fig.savefig(buf, format='jpeg')
    plt.close(fig)
    buf.seek(0)
    return buf.read()



def kline(
    title: str,
    data: list[dict]
) -> Optional[bytes]:
    """
    根據提供的資料繪製 K 線圖，並輸出為 JPEG 圖片的位元資料。

    參數:
        title (str): 圖表標題。
        data (list[dict]): 每筆資料需包含 open/high/low/close/date (開/高/低/收/日期) 的欄位。

    回傳:
        Optional[bytes]: 圖片的位元資料（JPEG 格式），可供儲存或回傳至前端。若資料無效則回傳 None。
    """
    if not data:
        return None

    x_labels = [item["date"] for item in data]
    x = list(range(len(x_labels)))

    fig, ax = plt.subplots(figsize=(max(8, len(data) * 0.3), 5))

    for i, item in enumerate(data):
        open_ = item["open"]
        close = item["close"]
        high = item["high"]
        low = item["low"]

        color = "red" if close >= open_ else "green"

        # 畫影線
        ax.plot([x[i], x[i]], [low, high], color=color)

        # 畫實體（開收之間的方塊）
        rect_y = min(open_, close)
        height = abs(open_ - close)
        ax.add_patch(plt.Rectangle(
            (x[i] - 0.3, rect_y), 0.6, height or 0.8,  # 如果漲跌幅是0，畫個小高度
            color=color
        ))

    ax.set_xticks(x)
    ax.set_xlim(-0.5, len(x) - 0.5)
    ax.set_xticklabels(x_labels, rotation=60, ha='right', fontproperties=font_prop)

    ax.set_title(title, fontproperties=font_prop)
    ax.set_xlabel("日期", fontproperties=font_prop)
    ax.set_ylabel("價格", fontproperties=font_prop)
    ax.grid(True)

    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format='jpeg')
    plt.close(fig)
    buf.seek(0)
    return buf.read()
