# Time Series Forecasting for Solar Home Electricity (New South Wales)

A PyTorch-based implementation of time series forecasting models for solar home electricity consumption/generation data from New South Wales, Australia. The dataset contains real-world residential electricity usage and solar generation data, enabling the evaluation of diverse forecasting models on practical time series scenarios.

## Dataset Information

Zip and CSV files are **not in git**. See the repository root `README.md` and `python scripts/fetch_data.py --list-sources`.

### Source

Ausgrid *Solar home electricity data*, 1 July 2012 – 30 June 2013 (`2012-2013 Solar home electricity data v2`). Historically listed on Data.NSW. Ausgrid no longer hosts the zip on their current site.

From the repository root, `python scripts/fetch_data.py --solar` writes the zip into this folder (original filename, with spaces). Then run `data_preprocess.py` to write `data_daily_long.csv`.

https://github.com/dimnoll/nsw-time-series-forecasting/releases/download/data-v1/2012-2013.Solar.home.electricity.data.v2.zip

### License

Dataset: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).  
**Attribution**: Ausgrid. For current information see www.ausgrid.com.au. Also listed historically by the State of New South Wales (www.nsw.gov.au).

Paper: E. L. Ratnam, S. R. Weller, C. M. Kellett, and A. T. Murray, “Residential load and rooftop PV generation: an Australian distribution network dataset,” *International Journal of Sustainable Energy*, 2017.

### Data Description

- Half-hour consumption and generation for 300 solar homes in the Ausgrid network
- Preprocess melts the wide CSV and aggregates to daily `daily_total_kWh` for next-day GG forecasting
- Covers multiple households with GC / CL / GG channels

## Implemented Models

### Deep Learning Models

- BiLSTM (Bidirectional Long Short-Term Memory)
- AM-BiLSTM (Attention Mechanism BiLSTM)
- TPA-BiLSTM (Temporal Pattern Attention BiLSTM)
- CNN-GRU (Convolutional Neural Network + Gated Recurrent Unit)
- DNN (Deep Neural Network)
- iTransformer (Improved Transformer for Time Series)

### Traditional Machine Learning Models

- RandomForest (Random Forest Regressor)
- XGBoost (Extreme Gradient Boosting)

## Core Utilities

- Data preprocessing pipeline for real-world time series data (handling missing values, normalization, feature engineering)
- Model training/evaluation utilities for non-tree-based models
- Dataset loading and transformation functions for PyTorch

## Requirements

The project uses Python 3.x and requires the following packages:

- numpy
- pandas
- scikit-learn
- torch
- matplotlib
- seaborn
- xgboost

---

# 新南威尔士州光伏住宅用电时间序列预测

基于 PyTorch 实现的时间序列预测模型，针对澳大利亚新南威尔士州（NSW）真实居民光伏住宅用电数据进行负荷/发电量预测。该数据集包含真实住宅的用电和光伏发电记录，可用于验证各类预测模型在实际时间序列场景中的性能。

## 数据集信息

zip / CSV **不进 git**。见仓库根 `README.md` 与 `python scripts/fetch_data.py --list-sources`。

### 数据源

Ausgrid *Solar home electricity data*（2012-07-01 至 2013-06-30）。曾挂在 Data.NSW；Ausgrid 现行站点已不提供 zip。仓库根目录运行 `python scripts/fetch_data.py --solar`，再跑 `data_preprocess.py`。

https://github.com/dimnoll/nsw-time-series-forecasting/releases/download/data-v1/2012-2013.Solar.home.electricity.data.v2.zip

### 授权协议

数据集：[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。署名 Ausgrid。论文：Ratnam et al., 2017。

### 数据说明

- 300 户半小时用电 / 光伏发电（GC / CL / GG）
- 预处理后得到按日 `daily_total_kWh`，用于次日 GG 总量预测

## 已实现模型

### 深度学习模型

- BiLSTM（双向长短期记忆网络）
- AM-BiLSTM（注意力机制双向长短期记忆网络）
- TPA-BiLSTM（时间模式注意力双向长短期记忆网络）
- CNN-GRU（卷积神经网络+门控循环单元）
- DNN（深度神经网络）
- iTransformer（改进型时间序列Transformer）

### 传统机器学习模型

- RandomForest（随机森林回归）
- XGBoost（极端梯度提升）

## 核心工具

- 面向真实世界时间序列的数据预处理流程（缺失值处理、标准化、特征工程）
- 非树基模型的训练/评估工具函数
- 适用于 PyTorch 的数据集加载与转换函数

## 依赖环境

项目使用 Python 3.x，需要以下包：
- numpy
- pandas
- scikit-learn
- torch
- matplotlib
- seaborn
- xgboost
