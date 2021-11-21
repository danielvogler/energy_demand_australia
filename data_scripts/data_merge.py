''' merge downloaded NEM data

1) appends data files for each year
2) merges all data sources (i.e., states) into one dataframe
3) produce smaller data samples by averaging

'''
import os
import sys
import glob
import shutil
from pathlib import Path
import pandas as pd
import yaml

script_dir = Path( os.path.split( os.path.abspath( sys.argv[0] ) )[0] )
config_file = script_dir / '../config/config.yaml'

with open(config_file, "r") as f:
  cfg = yaml.safe_load(f)
  
data_dir = script_dir / cfg['data']['data_path']
data_summary_dir = script_dir / cfg['data']['data_summary_path']

os.makedirs(data_summary_dir, exist_ok=True) 

states = cfg['data']['states']

for state in states:
    file_list = sorted( glob.glob( str( data_dir / '*{}*.csv'.format(state) ) ) )
    with open( data_summary_dir / str( cfg['data']['data_summary_prefix'] + state + '.csv') , 'wb') as summary_file:
        for i, file_name in enumerate(file_list):
                with open(file_name, 'rb') as sub_file:
                    if i != 0:
                        sub_file.readline() 
                    shutil.copyfileobj(sub_file, summary_file)
