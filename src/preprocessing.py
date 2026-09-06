import numpy as np
import pandas as pd


class SemiconductorPreprocessor:

  def __init__(self, data_path='../data/secom.data', labels_path='../data/secom_labels.data'):
    self.data_path = data_path
    self.labels_path = labels_path
    self.df = None

  def load_secom_data(self):
    """載入真實的 SECOM 半導體製造資料集"""
    try:
      # SECOM 資料是以空白鍵分隔的無標頭高維度矩陣
      data = pd.read_csv(self.data_path, sep=' ', header=None)
      labels = pd.read_csv(self.labels_path, sep=' ', header=None)

      # 組合特徵與標籤 (labels 的第 1 欄為 -1 正常, 1 異常)
      self.df = data.copy()
      self.df['Target'] = labels[0]

      print(f'【成功載入 SECOM 真實資料】')
      print(f'總筆數 (Samples): {self.df.shape[0]}')
      print(f'感測器特徵數 (Features): {self.df.shape[1] - 1}')
      return self.df
    except Exception as e:
      print(f'載入失敗，請確認 data 資料夾內是否有 secom.data 與 secom_labels.data。錯誤原因: {e}')
      return None

  def handle_missing_values(self):
    """處理半導體感測數據常見的缺失值 (以欄位平均值填補)"""
    if self.df is not None:
      # 保留 Target 欄位，僅對數值特徵補缺失值
      target = self.df['Target']
      features = self.df.drop(columns=['Target'])

      features = features.fillna(features.mean())
      self.df = pd.concat([features, target], axis=1)
      print('高維度感測器缺失值處理完成（已完成 Mean Imputation）。')
    return self.df

  def calculate_spc_limits(self, target_column):
    """計算特定感測器特徵的 SPC (Statistical Process Control) 統計管制界線"""
    if self.df is not None and target_column in self.df.columns:
      mean_val = self.df[target_column].mean()
      std_val = self.df[target_column].std()

      ucl = mean_val + 3 * std_val
      lcl = mean_val - 3 * std_val

      print(f'\n【SPC 統計分析 - 感測器 #{target_column}】')
      print(f'平均值 (Mean): {mean_val:.4f}')
      print(f'標準差 (Std): {std_val:.4f}')
      print(f'管制上限 (UCL): {ucl:.4f}')
      print(f'管制下限 (LCL): {lcl:.4f}')

      return mean_val, ucl, lcl
    else:
      raise ValueError(f'找不到欄位 {target_column}')


# 實際執行測試
if __name__ == '__main__':
  preprocessor = SemiconductorPreprocessor()
  df = preprocessor.load_secom_data()

  if df is not None:
    # 進行缺失值清洗
    preprocessor.handle_missing_values()

    # 以第 0 個感測器為例計算 SPC
    preprocessor.calculate_spc_limits(0)