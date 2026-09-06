# SmartFab-AI

### Semiconductor Process Monitoring & Anomaly Detection

以公開半導體製程資料集 SECOM 為基礎，建立一套製程數據分析與異常偵測系統。

本專案主要練習半導體製程資料的處理方式，並將統計分析、異常偵測模型與 REST API 整合，模擬實際製造環境中從資料整理、製程監控到異常判斷的流程。

---

## 專案背景

半導體製造過程會產生大量感測器與製程參數資料。當資料維度增加後，單純依靠固定門檻判斷異常，可能難以發現製程中的變化或異常樣本。

因此本專案以 SECOM 半導體製程資料集進行實作，從資料前處理開始，搭配統計分析與 Machine Learning 方法，嘗試建立一個簡單的製程異常偵測流程。

目前主要包含：

* 製程資料清理與缺失值處理
* 基本統計分析
* SPC 製程監控概念實作
* Isolation Forest 異常偵測
* FastAPI REST API
* AI 模型推論介面

---

## 使用資料集

本專案使用 **SECOM (Semiconductor Manufacturing Dataset)**。

資料包含約 1,500 筆製程樣本及 590 個感測器 / 製程特徵，部分欄位存在缺失值，因此需要在模型訓練前進行資料清理與處理。

### 資料內容

```text
secom.data
└── 製程感測器與製程參數

secom_labels.data
└── 製程結果標籤
```

本專案將標籤資料主要用於結果分析與模型評估，異常偵測模型本身則採用非監督式學習方式建立。

---

## 系統架構

```text
SECOM Dataset
      │
      ▼
Data Preprocessing
      │
      ├── Missing Value Handling
      ├── Feature Cleaning
      └── Data Transformation
      │
      ▼
Process Analysis
      │
      └── SPC / Statistical Analysis
      │
      ▼
Anomaly Detection
      │
      └── Isolation Forest
      │
      ▼
FastAPI
      │
      └── REST API
      │
      ▼
Prediction Result
```

---

## 專案結構

```text
SmartFab-AI/
│
├── data/
│   ├── secom.data
│   └── secom_labels.data
│
├── src/
│   ├── preprocessing.py
│   └── anomaly_model.py
│
├── api/
│   ├── __init__.py
│   └── main.py
│
├── .gitignore
└── README.md
```

### 主要模組

#### `preprocessing.py`

負責資料前處理，包括：

* SECOM 資料載入
* 缺失值處理
* 特徵資料整理
* 基本統計分析
* SPC 相關計算

#### `anomaly_model.py`

使用 **Isolation Forest** 建立非監督式異常偵測模型。

主要流程：

```text
Input Data
    ↓
Feature Processing
    ↓
Isolation Forest
    ↓
Anomaly Score
    ↓
Normal / Anomaly
```

#### `api/main.py`

使用 **FastAPI** 建立 REST API，將模型推論功能封裝成服務，方便後續與其他系統整合。

---

## 技術

| 類別                | 使用技術                       |
| ----------------- | -------------------------- |
| Programming       | Python                     |
| Data Processing   | Pandas, NumPy              |
| Machine Learning  | Scikit-learn               |
| Anomaly Detection | Isolation Forest           |
| API               | FastAPI                    |
| Data Analysis     | Statistical Analysis / SPC |
| Dataset           | SECOM                      |

---

## 目前完成項目

* [x] SECOM 資料載入
* [x] 缺失值處理
* [x] 製程資料整理
* [x] 基本統計分析
* [x] SPC 計算
* [x] Isolation Forest 異常偵測
* [x] FastAPI REST API
* [ ] Dashboard 視覺化
* [ ] 模型效能評估
* [ ] 異常特徵分析
* [ ] 即時資料串接

---

## 後續規劃

後續預計從目前的離線資料分析，逐步加入：

1. **製程數據視覺化**

   建立製程參數與異常資料的圖表，協助快速確認製程變化。

2. **異常特徵分析**

   分析異常樣本與正常樣本之間的差異，找出可能與異常相關的製程參數。

3. **模型評估**

   使用 Precision、Recall、F1-score 等指標評估異常偵測結果。

4. **API 整合**

   將模型推論功能透過 REST API 提供給其他應用程式使用。

5. **即時監控**

   未來可進一步串接模擬的製程資料流，建立接近實際產線的監控流程。

---

## 專案目的

這個專案主要希望將過去累積的 **軟體開發、資料庫與自動化經驗**，延伸到製程數據分析與 Machine Learning。

透過實際資料集進行開發，熟悉從資料處理、分析、模型建立到 API 整合的完整流程，也作為後續學習 **半導體製程、SPC、APC 與智慧製造** 的基礎。
