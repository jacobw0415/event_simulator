# Event Simulator

一個用於 **模擬事件資料** 並自動打進 REST API (`/events`) 的 Python 工具。  
支援 **X-Token 認證**、**自動刷新 Token**、**Graceful Shutdown**，方便測試 API 行為與驗證事件格式。

---

## 🚀 功能特色
- **事件模擬**：自動隨機產生不同裝置、網關、嚴重程度的事件。
- **定時推送**：可設定固定間隔（預設 5 秒）將事件送進 API。
- **X-Token 認證**：先呼叫 `/xauth` 取得 Token，再打 `/events`。
- **自動刷新 Token**：當 Token 過期 (`401 Unauthorized`) 時，自動重新取得新 Token。
- **Graceful Shutdown**：支援 `Ctrl+C` 或 `SIGTERM` 優雅結束。
- **可擴充事件模型**：不同 `CATEGORY` 可對應不同事件內容。

---

## 📂 專案結構
```
event_simulator/
├─ config.py           # API 與帳號設定
├─ main.py             # 主程式入口
└─ utils/
   └─ generator.py     # 隨機事件產生器
```

---

## ⚙️ 安裝方式

### 1. 建立虛擬環境
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

### 2. 安裝依賴
```bash
pip install requests
```

---

## 🔑 設定檔

在 `config.py` 調整參數：

```python
API_URL = "https://api.accelera-vs.com:8088/events"
XAUTH_URL = "https://api.accelera-vs.com:8088/xauth"

USERNAME = "admin"
PASSWORD = "admin"
GRANT_TYPE = "Password"

INTERVAL = 5         # 每隔幾秒送一次事件
CATEGORY = "GSS"     # 事件分類 (ESG / GSS / TOS / VaToxic / System)
```

---

## ▶️ 執行方式

```bash
python main.py
```

啟動後會自動：
1. 呼叫 `/xauth` 取得 X-Token
2. 每隔 `INTERVAL` 秒送一筆事件到 `/events`
3. 若 Token 過期，自動重新刷新
4. 按 `Ctrl+C` 即可 Graceful Shutdown

---

## 📊 範例輸出

```
✅ Got X-Token: eyJhbGciOi...
🚀 Event simulator started, sending to https://api.accelera-vs.com:8088/events every 5s
🔎 Debug -> URL: https://api.accelera-vs.com:8088/events
🔎 Debug -> Headers: {'X-Token': 'eyJhbGciOi...'}
[OK] TempSensor01 | Warning | Status 200
[OK] WaterLevel04 | Information | Status 200
[OK] CO2Sensor03 | Emergency | Status 200
🛑 Graceful Shutdown: Stopping event simulator...
✅ Event simulator stopped cleanly.
```

---

## 🛠 未來可擴充
- **事件分類更細緻化**：根據 `CATEGORY` 產生更真實的事件內容。
- **統計摘要**：結束程式時輸出送出事件總數與分佈。
- **Log 紀錄**：導出到檔案，支援日誌輪替。
- **CLI 參數**：支援 `--once`（單次事件）、`--interval <秒數>`。

---

## 📄 授權
本專案僅用於 **內部測試與開發**，不得用於生產環境。
