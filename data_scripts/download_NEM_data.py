''' file to download energy demand data from Australian states

from https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data

Example string passed to request:
url_address = "https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_202101_NSW1.csv"

'''

import os
import sys
from pathlib import Path

script_dir = Path( os.path.split( os.path.abspath( sys.argv[0] ) )[0] )
data_dir = script_dir / '../data/'

os.makedirs(data_dir, exist_ok=True) 

start_year = 2010
end_year = 2020

states = {"NSW","VIC","QLD","SA","TAS"}

url_prefix = "https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND"


for state in states:
  for year in range(start_year, end_year+1):
    for month in range(1,13): 
      url_address = url_prefix +  "_"  + str(year) +  str(month).zfill(2) +"_" + state + "1.csv"
      os.system( "wget {} -P {}".format(url_address, data_dir) )
