import streamlit as st
import pandas as pd

st.set_page_config(page_title='Net-Load Forecasting', page_icon=":sunny:", layout='wide')

'''
### 2-Year Data of 3 Regions in PJM

The data are collected from PJM's [Data Miner 2](https://dataminer2.pjm.com).
The PJM dataset includes hourly energy data (net meter and solar generation) for several regions in PJM.
The 3 selected regions are `MIDATL`, `SOUTH`, and `WEST`.
The data from 01/01/2019 to 06/30/2020 are used for training, and the data from 07/01/2020 to 12/31/2020 are used for testing.

Here are some considerations when preprocessing the data.
- We use `merge_asof` to map the timestamp in the net load data to the closest timestamp in the weather data.
- We fill missing (`NA`) values using `ffill` (using last valid observation to fill gap).
- We generate one data file for each region.
'''

st.code('''
df_19 = pd.read_csv('raw/hrl_load_metered_2019.csv', parse_dates=['datetime_beginning_utc', 'datetime_beginning_ept'])
df_20 = pd.read_csv('raw/hrl_load_metered_2020.csv', parse_dates=['datetime_beginning_utc', 'datetime_beginning_ept'])
df_all = pd.concat([df_19, df_20])
df_all = df_all[['datetime_beginning_utc', 'datetime_beginning_ept', 'mkt_region', 'mw']]
df_all = df_all.groupby(['datetime_beginning_utc','datetime_beginning_ept', 'mkt_region'], as_index=False).sum()
zones = ['MIDATL', 'SOUTH', 'WEST']
for zone in zones:
    df = df_all[df_all['mkt_region'] == zone].reset_index(drop=True).drop(['mkt_region'], axis=1)
    df.columns = ['utc', 'ept', 'mw']
    weather = pd.read_csv('raw/' + zone + '.csv', parse_dates=['valid']).drop(columns='station')
    weather = weather.rename(columns={'valid': 'utc'})
    weather = weather.fillna(method='ffill')
    df = pd.merge_asof(df, weather, on='utc')
    df.to_csv('data/' + zone + '.csv', index=False)
''')

'''
For machine learning purposes, we augment the feature space. As an example, we display the resulting dataframe for `MIDATL` as an interactive table.
- `month`: Month of the year, with `1` for January and `12` for December.
- `hour`: Hour of the day, from `0` to `23`.
- `dayofweek`: Day of the week, with `0` for Monday and `6` for Sunday.
- `mw_2`: 2-day lagged `mw`.
- `mw_7`: 7-day lagged `mw`.
'''

with st.echo():
    df = pd.read_csv('data/S4-MIDATL.csv', parse_dates=['utc', 'ept'])
    df['month'] = df['ept'].dt.month
    df['hour'] = df['ept'].dt.hour
    df['dayofweek'] = df['ept'].dt.dayofweek
    df['mw_2'] = df['mw'].shift(24 * 2)
    df['mw_7'] = df['mw'].shift(24 * 7)
    df
