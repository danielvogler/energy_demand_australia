''' file to download and pre-process energy demand data from Australian states

from https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data

Example string passed to request:
url_address = "https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_202101_NSW1.csv"

'''

import os
import sys
import yaml
from data_utils import DataUtils

DataUtils()

states = DataUtils().states
start_year = DataUtils().start_year
end_year = DataUtils().end_year

if DataUtils().data_download:
  DataUtils().download_monthly_data( states, start_year, end_year)

if DataUtils().data_preprocess:
  for state in states:
    DataUtils().merge_monthly_data(state)
    df_state, df_state_avg = DataUtils().create_df(state, avg_window=DataUtils().avg_window)
    DataUtils().plot_time_series(df_state_avg, state)
  
  df_all = DataUtils().merge_dfs( str( DataUtils().data_summary_prefix + 'avg_'), name_str=DataUtils().avg_window)
  DataUtils().plot_all_time_series(df_all)
print(df_all.head())