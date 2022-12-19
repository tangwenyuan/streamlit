import streamlit as st

st.set_page_config(page_title='Net-Load Forecasting', page_icon=":sunny:", layout='wide')

'''
## Data Preprocessing

In this project, we collect 5 small data sets (S1 to S5) and 5 large data sets (L1 to L5).
- Small data set: A data set with a time horizon of 3 years or less.
- Large data set: A data set with a time horizon of more than 3 years.

The raw data, either from public repositories or partner utilities, may be incorrect, incomplete, or inadequately formatted.
Thus, we need to preprocess the raw data to generate clean data sets for the development of machine learning models.
Here are some considerations when preprocessing the raw data.

### Metadata

Metadata is "data that provides information about other data", or "data about data".
'''

tabs = st.tabs(['Time zone', 'Time interval', 'Unit of measurement'])

with tabs[0]:
    '''
    The timestamp can be in local time, e.g., Eastern Prevailing Time (EPT), or in Coordinated Universal Time (UTC).

    Prevailing time is the time on an automatically updated clock, according to the conventions for the time and the location.
    For example, Eastern Prevailing Time (EPT) can be either Eastern Standard Time (EST) or Eastern Daylight Time (EDT), depending on the date.

    UTC does not observe daylight saving time.

    Prevailing time is easier to interpret, while UTC avoids the ambiguity arising from the daylight saving time.
    '''

with tabs[1]:
    '''
    Consider hourly data. For each observation, the timestamp can be either the beginning (which is more common) or the end of the one-hour interval.

    If it is the beginning, then `2022-01-01 00:00:00` means the interval between `2022-01-01 00:00:00` and `2022-01-01 01:00:00`.

    Sometimes the timestamp is represented by date and hour separately. Then it is important to know whether the first hour is coded as hour `0` or hour `1`,
    and how the extra hour during the shift from daylight savings time to standard time is coded.
    '''

with tabs[2]:
    '''
    For load and solar generation, it is important to know whether the unit is kW or MW.

    For temperature, it is important to know whether the unit is degree Celsius or degree Fahrenheit.
    '''

'''
### Time Zone Conversion

It is convenient to have both UTC and local time in the data sets.

When only the local time is available in the raw data sets, we need to pay special attention to how the extra hour during the shift from daylight savings time to standard time is coded.

The [list of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) is useful for time zone conversion. For example, `America/New_York` and `US/Eastern` mean the same.

### Timestamp Consistency

Load, solar generation, weather, etc., may come from different data files, and hence may use different conventions of time zones.

The difference between EPT and UTC may be obvious, but the difference between EST and EDT is much more subtle.

It is important to check the timestamp consistency between different data sets.

### Sanity Check

While it is hard to identify all the issues in the raw data sets, we can conduct sanity check to quickly identify apparent issues.

For example, we can count the number of observations. For hourly data, there should be 8760 observations in a common year and 8784 observations in a leap year.
Sometimes the extra hour during the shift from daylight savings time to standard time is aggregated or averaged with the preceding hour, or simply removed, which we should pay attention to.

We can also conduct exploratory data analysis, through summary statistics, data visualization, etc., to identify outliers that may be incorrect values in the data sets.

### Missing Values

Missing values are common in raw data sets. There can be scattered or sequential missing values.

We can either remove the corresponding observations, or fill the missing values.
- We can replace the missing values by specific values, such as `0` or the average value of that column.
- We can use either the last or the next valid observation to fill the gap.
- We can use domain knowledge to fill the missing values.
'''
