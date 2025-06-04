from dotenv import load_dotenv
load_dotenv(".env.local")
from api.webhook import app

if __name__ == "__main__":
    # 這樣可以在本地與 Render 都正常啟動
    import os
    port = int(os.environ.get("PORT", 5000))  # Render 預設會傳入 PORT 環境變數
    app.run(host="0.0.0.0", port=port)