# Group LineBot

LINE 群組聊天機器人，提供多種實用與趣味功能。

## 功能

- **擲骰子 / 丟骰子** — 隨機擲骰
- **擲硬幣 / 丟硬幣** — 隨機擲硬幣
- **天氣預報** — 查詢台灣各地天氣
- **台股** — 查詢台股即時價格
- **Mygo 圖包** — 自動回應 Mygo 相關圖片
- **衛星雲圖** — 取得最新衛星雲圖
- **使用說明** — 查看功能列表

## 安裝與啟動

```bash
pip install -r requirements.txt
```

在專案根目錄建立 `.env` 檔案，填入以下環境變數：

| 變數 | 說明 |
|---|---|
| `CHANNEL_ACCESS_TOKEN` | LINE Channel Access Token |
| `CHANNEL_SECRET` | LINE Channel Secret |
| `MOTC_API` | 中央氣象署 Open Data API Key |
| `TIMEZONE` | 時區（預設 `Etc/GMT-8`） |
| `MYGO_BASE_URL` | Mygo 圖片的公開 URL 前綴 |

啟動伺服器：

```bash
python app.py
```

將 LINE webhook URL 設定為 `https://<your-domain>/callback`。

## 技術

- Python / Flask
- LINE Messaging API（line-bot-sdk）
- BeautifulSoup（網頁爬蟲）
- aiohttp（非同步 HTTP 請求）
