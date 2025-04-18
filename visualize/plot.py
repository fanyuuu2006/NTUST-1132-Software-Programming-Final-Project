from io import BytesIO
from typing import Literal, Optional
import matplotlib.pyplot as plt
from matplotlib import rcParams, font_manager


# 設定中文字型與負號顯示
font_path = "assets/fonts/NotoSansTC-Regular.ttf"
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

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

    # 畫圖
    fig, ax = plt.subplots(figsize=(max(8, len(x_data) * 0.3), 5))
    # 建立漲跌分組
    up_segments = []
    down_segments = []

    for i in range(1, len(x_data)):
        segment = ([x_data[i - 1], x_data[i]], [y_data[i - 1], y_data[i]])
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
    ax.set_xticklabels(x_data, rotation=60, ha='right')

    ax.set_title(title)
    ax.set_xlabel(y_label)
    ax.set_ylabel(x_label)
    ax.grid(True)

    fig.tight_layout()

    # 圖轉為 bytes
    buf = BytesIO()
    fig.savefig(buf, format='jpeg')
    plt.close(fig)
    buf.seek(0)
    return buf.read()



