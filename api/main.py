import os
from fastapi import FastAPI
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

app = FastAPI(
    title="SmartFab-AI Semiconductor API",
    description="結合 SECOM 真實資料集與 Isolation Forest 的產線 AI 異常偵測 API",
    version="2.0.0",
)


@app.get("/")
def home():
  return {
      "status": "online",
      "message": "SmartFab-AI API is running successfully!",
  }


@app.get("/predict/real-sample")
def predict_real_sample():
  """直接從真實的 secom.data 讀取第一筆晶圓感測數據進行 AI 異常檢測"""
  try:
    # 使用絕對路徑防範不同資料夾啟動時找不到檔案的問題
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "secom.data")
    labels_path = os.path.join(base_dir, "data", "secom_labels.data")

    # 讀取真實資料檔案
    data = pd.read_csv(data_path, sep=" ", header=None)
    labels = pd.read_csv(labels_path, sep=" ", header=None)

    # 補齊缺失值（與前置處理邏輯一致）
    data = data.fillna(data.mean())

    # 取出第一筆資料（590個特徵）
    sample_features = data.iloc[0].values.tolist()
    true_label = int(labels.iloc[0, 0])

    # 訓練簡單模型進行預測
    model = IsolationForest(contamination=0.07, random_state=42)
    model.fit(data)

    # 進行預測
    prediction = int(model.predict([sample_features])[0])
    status_str = (
        "Normal" if prediction == 1 else "Abnormal (Anomaly Detected)"
    )

    return {
        "source": "SECOM Real Dataset (Row 0)",
        "sensor_count": len(sample_features),
        "ai_prediction": prediction,
        "ai_status": status_str,
        "true_historical_label": (
            "Normal (-1)" if true_label == -1 else "Abnormal (1)"
        ),
    }
  except Exception as e:
    return {
        "error": f"讀取真實資料失敗，請確認 data/ 內是否有 secom.data 檔案。原因: {str(e)}"
    }