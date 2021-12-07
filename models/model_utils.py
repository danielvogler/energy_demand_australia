'''

'''
import os
import sys
import yaml
import glob
from pathlib import Path
import pandas as pd

class ModelUtils:

    def __init__(self):
        ''' global definitions'''
        self.script_dir = Path( os.path.split( os.path.abspath( sys.argv[0] ) )[0] )
        self.config_file = self.script_dir / '../config/config.yaml'

        with open( self.config_file, "r") as f:
            cfg = yaml.safe_load(f)

        self.data_download = cfg['data']['data_download']
        self.data_preprocess = cfg['data']['data_preprocess']
        self.start_year = cfg['data']['start_year']
        self.end_year = cfg['data']['end_year']
        self.states = cfg['data']['states']
        self.data_dir = self.script_dir / cfg['data']['data_path']
        self.data_summary_dir = self.script_dir / cfg['data']['data_summary_path']
        self.url_prefix = cfg['data']['url_prefix']
        self.data_summary_prefix = cfg['data']['data_summary_prefix']
        self.avg_window = cfg['data']['avg_window']

        self.fig_dir = self.script_dir / cfg['plot']['fig_path']

        self.initialize_dirs()

        return


    def initialize_dirs(self):
        ''' intialize some necessary directories'''
        os.makedirs( self.data_dir, exist_ok=True) 
        os.makedirs( self.data_summary_dir, exist_ok=True) 
        os.makedirs( self.fig_dir, exist_ok=True) 
        return

        
    def load_summary_df(  self,
                    df_prefix:str=None,
                    name_str:str=None):
        ''' LOad summary dataframe '''
        
        df = pd.read_pickle( self.data_summary_dir / str( self.data_summary_prefix + name_str + '_all.pkl') )
        return df