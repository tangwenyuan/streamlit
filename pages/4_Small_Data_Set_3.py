import streamlit as st
import pandas as pd

st.set_page_config(page_title='Net-Load Forecasting', page_icon=":sunny:", layout='wide')

'''
### 3-Year Data of 14 Countries in Europe

The data are collected from the [Open Power System Data](https://open-power-system-data.org) (OPSD).
The OPSD dataset includes hourly energy data (net meter and solar generation) and weather data for several countries in Europe from 01/01/2015 to mid 2020.
The data from 01/01/2017 to 12/31/2018 are used for training, and the data from 01/01/2019 to 12/31/2019 are used for testing.

Here are some considerations when preprocessing the data.
- The names of the countries can be extracted from the column names.
- We fill missing (`NA`) values using `bfill` (using next valid observation to fill gap).
- We generate one data file for each country.
'''

st.code('''
df_demand = pd.read_csv('raw/demand_data.csv', parse_dates=['utc_timestamp'])
df_weather = pd.read_csv('raw/weather_data.csv')
df_utc = pd.DataFrame({'utc': df_demand['utc_timestamp'].dt.tz_convert(None)})
zones = [x[:2] for x in df_demand.columns[1::2]]
for i in range(len(zones)):
    df = df_utc.copy()
    df['mw'] = df_demand.iloc[:, i * 2 + 1]
    df['tmpc'] = df_weather.iloc[:, i * 3 + 1]
    df = df.fillna(method='bfill')
    df = df[df['utc'].dt.year.between(2017, 2019)]
    df.to_csv('data/S3-' + zones[i] + '.csv', index=False)
''')

'''
For machine learning purposes, we augment the feature space. As an example, we display the resulting dataframe for Austria (`AT`) as an interactive table.
- `month`: Month of the year, with `1` for January and `12` for December.
- `hour`: Hour of the day, from `0` to `23`.
- `dayofweek`: Day of the week, with `0` for Monday and `6` for Sunday.
- `mw_2`: 2-day lagged `mw`.
- `mw_7`: 7-day lagged `mw`.
'''

with st.echo():
    df = pd.read_csv('data/S3-AT.csv', parse_dates=['utc'])
    df['month'] = df['utc'].dt.month
    df['hour'] = df['utc'].dt.hour
    df['dayofweek'] = df['utc'].dt.dayofweek
    df['mw_2'] = df['mw'].shift(24 * 2)
    df['mw_7'] = df['mw'].shift(24 * 7)
    df
