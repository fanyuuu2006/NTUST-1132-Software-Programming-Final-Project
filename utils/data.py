import json
import base64
import gzip  # GNU zip，資料壓縮工具
from io import BytesIO

def compress_data(data: dict | list) -> str:
    """
    將 dict 或 list 資料壓縮後轉換為 base64-url 格式字串，可用於網址中傳輸。

    參數：
        data (dict | list): 欲壓縮的資料，例如 stock_data。

    回傳：
        str: 壓縮後並轉為可放入網址的 base64-url 字串。
    """
    # 將資料轉成 JSON 字串
    json_str = json.dumps(data, ensure_ascii=False)

    # 建立一個記憶體中的位元緩衝區（類似檔案的容器）
    buf = BytesIO()

    # 使用 gzip 壓縮 JSON 字串，寫入 buffer 中
    with gzip.GzipFile(fileobj=buf, mode="wb") as f:
        f.write(json_str.encode("utf-8"))

    # 取得壓縮後的 bytes 資料
    compressed = buf.getvalue()

    # 將壓縮資料進行 base64-url 編碼（適合放在網址中），再轉成字串回傳
    return base64.urlsafe_b64encode(compressed).decode("utf-8")



def decompress_data(token: str) -> dict|list:
    """
    將 base64-url 字串還原為原始資料（dict 或 list）。

    參數：
        token (str): 壓縮過並編碼的字串（來自 compress_data() 的輸出）。

    回傳：
        dict|list: 解壓縮並解析後的原始資料（與壓縮前一致）。
    """
    # 將 base64-url 字串還原成原始壓縮的 bytes
    compressed = base64.urlsafe_b64decode(token)

    # 解壓縮 gzip 資料，並轉回 JSON 字串 → 再解析成 Python dict
    with gzip.GzipFile(fileobj=BytesIO(compressed), mode="rb") as f:
        return json.loads(f.read().decode("utf-8"))
