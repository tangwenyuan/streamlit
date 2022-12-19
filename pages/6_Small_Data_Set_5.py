import streamlit as st
import pandas as pd

st.set_page_config(page_title='Net-Load Forecasting', page_icon=":sunny:", layout='wide')

'''
### 3-Year Data of 1 Delivery Point in NCEMC

The S5 dataset includes hourly net load data of 1 delivery point in the NCEMC, along with the utility-scale solar generation data at that delivery point.
The data from 01/01/2019 to 12/31/2020 are used for training, and the data from 01/01/2021 to 12/31/2021 are used for testing.

Here are some considerations when preprocessing the data.
- The timestamp is represented by two columns `meas_dt` (e.g., `20190101`) and `meas_hr` (from `1` to `25`).
- The missing hour during the shift from standard time to daylight savings time has a `meas_hr` value of `2`, which should be `3` for consistency.
- The extra hour during the shift from daylight savings time to standard time has a `meas_hr` value of `25`, which is out of chronological order.
- We fill missing (`NA`) values using `ffill` (using last valid observation to fill gap).
- We use `merge_asof` to map the timestamp in the net load data to the closest timestamp in the weather data.
'''

st.code('''
df = pd.read_csv('raw/load_solar_out.csv')
df = df[df['meter_name'] == 'Delivery Point'] # For data desensitization, the actual name is masked with 'Delivery Point'
df = df.drop(['meter_cd', 'meter_name', 'cust_cd'], axis=1)
df['meas_dt'] = pd.to_datetime(df['meas_dt'].astype(str))
df['ept'] = df['meas_dt'] + pd.to_timedelta(df['meas_hr'] - 1, 'h')
df.loc[df['meas_hr'] == 25, 'ept'] -= pd.to_timedelta(23, 'h')
df = df.sort_values(['ept', 'meas_hr'])
df['ept'] = df['ept'].dt.tz_localize('US/Eastern', ambiguous='infer', nonexistent=pd.to_timedelta(-1, 'h'))
df['utc'] = df['ept'].dt.tz_convert(None)
df['ept'] = df['ept'].dt.tz_localize(None)
df = df[['utc', 'ept', 'kw_meas']].reset_index(drop=True)
df = df.rename(columns={'kw_meas': 'kw'})
weather = pd.read_csv('raw/GWW.csv', parse_dates=['valid']).drop(columns='station')
weather = weather.rename(columns={'valid': 'utc'})
weather = weather.fillna(method='ffill')
df = pd.merge_asof(df, weather, on='utc')
df = df[df['ept'].dt.year.between(2019, 2021)]
df.to_csv('data/S5-dp.csv', index=False)
''')

'''
For machine learning purposes, we augment the feature space, and display the first few rows of the resulting dataframe (for data desensitization).
- `month`: Month of the year, with `1` for January and `12` for December.
- `hour`: Hour of the day, from `0` to `23`.
- `dayofweek`: Day of the week, with `0` for Monday and `6` for Sunday.
- `kw_2`: 2-day lagged `kw`.
- `kw_7`: 7-day lagged `kw`.
'''

with st.echo():
    df = pd.read_csv('data/S5-dp.csv', parse_dates=['utc', 'ept'])
    df['month'] = df['ept'].dt.month
    df['hour'] = df['ept'].dt.hour
    df['dayofweek'] = df['ept'].dt.dayofweek
    df['kw_2'] = df['kw'].shift(24 * 2)
    df['kw_7'] = df['kw'].shift(24 * 7)
    st.write(df.head())
