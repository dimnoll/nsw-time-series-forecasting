# nsw-time-series-forecasting

[English](#english) | [中文](#中文)

Personal time-series forecasting experiments on New South Wales electricity: synthetic load, Ausgrid solar-home meters, and AEMO NSW1 demand / price.

Code is MIT (`dimnoll`). CSV and zip files stay out of git; fetch or generate them with `scripts/fetch_data.py`. A GitHub Release can hold a frozen `data-pack.zip`.

Earlier public copy: https://github.com/dimnoll/TimeSeriesForecasting  
That repository is being made private. Its commits used a personal email, and it stored the datasets in git.

---

## English

### Layout

```text
tf-syndt/                 TensorFlow/Keras on synthetic 15-minute load
th-nsw-solar-home/        PyTorch on Ausgrid solar-home daily kWh
th-nsw-demand-price/      PyTorch: next 48 half-hours of NSW1 demand and RRP
scripts/fetch_data.py     generate / download / unpack a Release
scripts/pack_data.py      zip local datasets for a Release
requirements-tf.txt
requirements-torch.txt
```

### Data (not committed)

| Experiment | What to get | Licence / attribution |
| --- | --- | --- |
| `tf-syndt` | `python scripts/fetch_data.py --synthetic` | generated here |
| `th-nsw-solar-home` | Ausgrid *Solar home electricity data*, 1 Jul 2012 – 30 Jun 2013 (`2012-2013 Solar home electricity data v2`) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Ausgrid; historically listed on [Data.NSW](https://data.nsw.gov.au/). Paper: Ratnam et al., *International Journal of Sustainable Energy*, 2017 |
| `th-nsw-demand-price` | `python scripts/fetch_data.py --aemo` then `data_preprocess.py` | [AEMO aggregated price and demand](https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data). Attribute AEMO as the author of that material |

Ausgrid no longer hosts that zip. A CC BY 4.0 copy can live on this machine and later on a Release; it does not go into git. Put the zip (or unzipped CSV) in `th-nsw-solar-home/`, or unpack a Release pack.

After a `data-v1` Release exists:

```text
python scripts/fetch_data.py --from-release
```

`python scripts/fetch_data.py --list-sources` prints the URLs.

### Models

Statistical: ARIMA, ARIMAX. Deep learning: BiLSTM, AM-BiLSTM, TPA-BiLSTM, CNN-GRU, DNN, iTransformer. Tree: XGBoost. KAN scripts are present but optional (`pykan`).

`th-nsw-demand-price` predicts the next **48 half-hours** of `TOTALDEMAND` and `RRP` from a 336-step lookback (one week). Evaluation HTML from a completed run is in `th-nsw-demand-price/results/` (metrics only, not the series).

### Setup

TensorFlow experiments:

```text
pip install -r requirements-tf.txt
python scripts/fetch_data.py --synthetic
```

PyTorch experiments:

```text
pip install -r requirements-torch.txt
python scripts/fetch_data.py --aemo
```

Then run preprocess and model scripts from each subfolder, as those files expect.

---

## 中文

个人时序预测实验：合成负荷、Ausgrid 光伏户表、AEMO NSW1 负荷与电价。

代码 MIT，著作权人 **dimnoll**。CSV / zip 不进 git，用 `scripts/fetch_data.py` 生成、下载或解开 Release。

先前的公开副本：https://github.com/dimnoll/TimeSeriesForecasting  
该仓库将改为私有：提交记录里有个人邮箱，而且数据集进了 git。

### 数据（不提交）

- 合成负荷：`--synthetic`
- 光伏户表：Ausgrid 2012–2013，CC BY 4.0。官网 zip 已下线；本机或 Release 可保留一份，不进 git
- 负荷电价：`--aemo` 拉 NSW1 月文件，再跑 `data_preprocess.py`；须署名 AEMO

`th-nsw-demand-price` 用过去一周（336 个半小时）预测未来 48 个半小时的 `TOTALDEMAND` 与 `RRP`。
