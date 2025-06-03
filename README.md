# 📈 玩股票都不揪 - LINE 股票查詢小幫手

![GitHub Created At](https://img.shields.io/github/created-at/fanyuuu2006/NTUST-1132-Software-Programming-Final-Project) ![GitHub Last Commit](https://img.shields.io/github/last-commit/fanyuuu2006/NTUST-1132-Software-Programming-Final-Project)

## 🧠 專案介紹

本專案為 113 學年度 第 2 學期 資訊管理系「程式設計」課程期末專題，旨在打造一個結合 **LINE Bot** 、 **股市資料爬蟲** 與 **視覺化資料** 的互動式系統，讓使用者能夠在 LINE 上透過指令即時查詢台灣股票資訊，包括即時股價、每日交易資訊、股票名稱、收盤價趨勢圖與K線圖等。

---

## 💡 使用方式

使用者只需在 LINE 中輸入簡單指令，即可快速獲取股票資訊

---

## 🧱 系統架構

### 🔧 技術與模組

- **語言**：Python 3.12
- **架構**：Flask + Line Messaging API
- **資料來源**：[台灣證券交易所（TWSE）](https://www.twse.com.tw/)公開 API
- **功能模組**：
  - `crawler/`：爬蟲模組，負責抓取即時與歷史股票資料
  - `api/`：LINE Bot 指令控制器與回應處理
  - `visualize/`：使用 Matplotlib 繪製資料視覺化圖片模組
  - `utils/`：輔助函式模組（日期轉換、網址縮短等）

---

## 📊 成果示例

使用 `/kline 2330 20250101 20250418` 指令，系統將產生以下風格的K線圖（紅色表示上漲、綠色表示下跌、黑色則不變）：

![K Line Example](https://tinyurl.com/28ycbplh)

---

## 👨‍👩‍👧‍👦 組員資訊

> NTUST 資訊管理系 大一下

- B11309014 何采妮
- B11309019 陳立翔
- B11309041 林芮菁
- B11309044 范余振富
- B11309056 徐浩郡
- B11309059 尤薇嫚

---

## 🚀 如何使用

1. 加入我們的 LINE Bot
2. 輸入 `/help` 查看所有可用功能
3. 開始玩股票！📉📈

---

## 📌 注意事項

- 本系統為課程專案，資料非即時專業投資建議
- 若圖表無法顯示，請嘗試將網址貼至瀏覽器開啟
- 圖表資料過多時將自動簡化或發出錯誤提示

---

## 🤝 貢獻

有任何問題或建議歡迎提交 [Issue](https://github.com/fanyuuu2006/NTUST-1132-Software-Programming-Final-Project/issues/new)
