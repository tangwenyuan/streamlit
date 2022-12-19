import streamlit as st
import pandas as pd

st.set_page_config(page_title='Net-Load Forecasting', page_icon=":sunny:", layout='wide')

'''
### 1-Year Data of Selected Sites in North America

The data are collected from the SunDance dataset in the [UMass Trace Repository](http://traces.cs.umass.edu).
The SunDance dataset includes hourly energy data (net meter and solar generation) and weather data
(weather condition data from public weather stations and APIs) for 100 solar sites in North America from 01/01/2015 to 12/31/2015.
The sites in the Mountain Time Zone are selected, the aggregated net load of which is considered as the target.
The data from 01/01/2015 to 10/31/2015 are used for training, and the remaining data are used for testing.

First, we select the sites with time zone `America/Denver` (the Mountain Prevailing Time).
'''

st.code('''
path = 'raw/SunDance_data_release/weather/'
files = []
for file in listdir(path):
    if file.startswith('SunDance'):
        f = open(path + file, 'r')
        if 'Denver' in f.readline():
            files.append(file)
''')

'''
Then, we aggregate the net load of the selected sites.
- Some filenames are in the form of `SunDance_1007.csv`, while others are in the form of `SunDance_10010_data.csv`.
- Only those with a complete year of data and the `Grid [kW]` (net load) column are retained.
- The original observations in each file are in the reverse chronological order.
- The original timestamps are in the Mountain Prevailing Time, which is converted to UTC.
'''

st.code('''
path = 'raw/SunDance_data_release/energy/'
df = pd.DataFrame({'utc': [], 'mpt': [], 'kw': []})
for file in files:
    if isfile(path + file):
        df1 = pd.read_csv(path + file, parse_dates=['Date & Time'])
    else:
        df1 = pd.read_csv(path + file[:-4] + '_data.csv', parse_dates=['Date & Time'])
    if (len(df1) >= 8760) and ('Grid [kW]' in df1.columns):
        df1['mpt'] = df1['Date & Time']
        df1 = df1[df1['mpt'].dt.year == 2015][::-1]
        df1['mpt'] = df1['mpt'].dt.tz_localize('US/Mountain', ambiguous='infer')
        df1['utc'] = df1['mpt'].dt.tz_convert(None)
        df1['mpt'] = df1['mpt'].dt.tz_localize(None)
        df1['kw'] = df1['Grid [kW]']
        df = pd.concat([df, df1[['utc', 'mpt', 'kw']]])
df = df.groupby(['utc', 'mpt'], as_index=False).sum()
''')

'''
We collect the weather data (in particular, `tmpf`, temperature in degree Fahrenheit).
- The timestamps are in UTC to avoid the ambiguity due to the daylight saving time.
- Fill missing (`NA`) values using `ffill` (using last valid observation to fill gap).
- Use `merge_asof` to map the timestamp in the net load data to the closest timestamp in the weather data.
'''

st.code('''
weather = pd.read_csv('raw/DEN.csv', parse_dates=['valid']).drop(columns='station')
weather = weather.rename(columns={'valid': 'utc'})
weather = weather.fillna(method='ffill')
df = pd.merge_asof(df, weather, on='utc')
df.to_csv('data/S1.csv', index=False)
''')

'''
For machine learning purposes, we augment the feature space, and display the resulting dataframe as an interactive table.
- `month`: Month of the year, with `1` for January and `12` for December.
- `hour`: Hour of the day, from `0` to `23`.
- `dayofweek`: Day of the week, with `0` for Monday and `6` for Sunday.
- `kw_2`: 2-day lagged `kw`.
- `kw_7`: 7-day lagged `kw`.
'''

with st.echo():
    df = pd.read_csv('data/S1.csv', parse_dates=['utc', 'mpt'])
    df['month'] = df['mpt'].dt.month
    df['hour'] = df['mpt'].dt.hour
    df['dayofweek'] = df['mpt'].dt.dayofweek
    df['kw_2'] = df['kw'].shift(24 * 2)
    df['kw_7'] = df['kw'].shift(24 * 7)
    df
