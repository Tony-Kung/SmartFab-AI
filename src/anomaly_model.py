import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from preprocessing import SemiconductorPreprocessor


class SecomAnomalyModel:

  def __init__(self, contamination=0.07):
    """初始化 Isolation Forest 異常偵測模型

    SECOM 資料集中異常品約佔 6.6%，故 contamination 設為 0.07
    """
    self.model = IsolationForest(contamination=contamination, random_state=42)

  def run_detection(self, df):
    """對 SECOM 高維度感測器數據進行機器學習異常偵測"""
    # 移除最後的 Target 標籤欄位，只留下 590 個感測器數值
    X = df.drop(columns=['Target'])

    print('\n【正在訓練 Isolation Forest 模型並進行產線異常檢測...】')
    self.model.fit(X)

    # 預測：-1 代表模型判定異常，1 代表正常
    predictions = self.model.predict(X)
    df['AI_Anomaly_Pred'] = predictions

    anomalies = df[df['AI_Anomaly_Pred'] == -1]

    print(f'總檢測晶圓/批次數: {len(df)}')
    print(f'AI 偵測出的異常筆數: {len(anomalies)}')
    return df


if __name__ == '__main__':
  # 1. 載入並清洗真實資料
  prep = SemiconductorPreprocessor()
  df = prep.load_secom_data()

  if df is not None:
    df = prep.handle_missing_values()

    # 2. 執行 AI 異常檢測
    detector = SecomAnomalyModel(contamination=0.07)
    result_df = detector.run_detection(df)

    print('\n前 5 筆 AI 異常檢測結果預覽：')
    print(result_df[['AI_Anomaly_Pred', 'Target']].head())