# NSW1 demand and price (half-hour)

PyTorch models for the next **48 half-hours** of AEMO NSW1 `TOTALDEMAND` (MW) and `RRP` ($/MWh). Lookback is 336 steps (seven days). Window in the processed files: July 2012 – June 2013.

This folder was not documented in the earlier experiment dump; the task is `tasks/next_48h_forecast.py`.

## Data (gitignored)

1. `python scripts/fetch_data.py --aemo` from the repo root (writes `data_csvs/`).
2. `python data_preprocess.py` from this folder (writes `data_processed/nsw_halfhour_201207_201306.csv`).
3. `python main.py`.

Source: [AEMO aggregated price and demand](https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data). Attribute AEMO.

`results/*.html` are metric tables from a finished comparison (before/after a simple bias correction). They are not the time series.

## Models

CNN-GRU, BiLSTM, TPA-BiLSTM, AM-BiLSTM, DNN, iTransformer (`lucidrains` package). Config is `config.py`.
