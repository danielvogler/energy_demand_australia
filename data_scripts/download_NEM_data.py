''' file to download energy demand data from Australian states

from https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data

Example string passed to request:
url_address = "https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_202101_NSW1.csv"

'''

import os
import sys
from pathlib import Path
import yaml

script_dir = Path( os.path.split( os.path.abspath( sys.argv[0] ) )[0] )
config_file = script_dir / '../config/config.yaml'

with open(config_file, "r") as f:
  cfg = yaml.safe_load(f)

data_dir = script_dir / cfg['data']['data_path']

os.makedirs(data_dir, exist_ok=True) 

start_year = cfg['data']['start_year']
end_year = cfg['data']['end_year']

states = cfg['data']['states']

### load data for states and months
for state in states:
  for year in range(start_year, end_year+1):
    for month in range(1,13): 
      url_address = cfg['data']['url_prefix'] +  "_"  + str(year) +  str(month).zfill(2) +"_" + state + "1.csv"
      os.system( "wget {} -P {}".format(url_address, data_dir) )
