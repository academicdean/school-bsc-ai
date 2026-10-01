# STREAMING_CHUNK:建立專案的 README 說明文件...
# 🎯 能動平衡計分卡 AI 引導系統

這是一個基於 Python Streamlit 與 OpenAI API 開發的校務治理輔助系統。系統扮演「引導教練」的角色，透過分步對話協助高中校務團隊將抽象的學校願景，轉化為具體的策略地圖與數據化指標。

## 功能特色
- **四步引導精靈**：從願景盤點、構面行動挑選、KPI 設計到行為數據化落實。
- **AI 專業建議**：整合 GPT-4o 模型，鎖定「高中校務治理專家」角色，避免生硬商業術語。
- **一鍵匯出**：最終策略地圖可直接匯出為 CSV 格式，方便使用 Excel 開啟並帶入校務會議討論。

## 本地端執行方式

1. 安裝所需套件：
```bash
pip install -r requirements.txt
```

2. 啟動 Streamlit 伺服器：
```bash
streamlit run app.py
```

3. 系統將自動於瀏覽器開啟 `http://localhost:8501`。請於介面左側輸入您的 OpenAI API Key 即可開始使用。

## 部署建議
本專案已備妥 `requirements.txt`，非常適合直接部署於 [Streamlit Community Cloud](https://share.streamlit.io/) 進行免費託管。