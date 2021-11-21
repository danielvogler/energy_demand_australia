'''

'''
import os
import sys
import yaml
from pathlib import Path

class DataUtils:

    def __init__(self):
        ''' global definitions'''
        self.script_dir = Path( os.path.split( os.path.abspath( sys.argv[0] ) )[0] )
        self.config_file = self.script_dir / '../config/config.yaml'

        with open( self.config_file, "r") as f:
            cfg = yaml.safe_load(f)

        self.start_year = cfg['data']['start_year']
        self.end_year = cfg['data']['end_year']
        self.states = cfg['data']['states']
        self.data_dir = self.script_dir / cfg['data']['data_path']
        self.data_summary_dir = self.script_dir / cfg['data']['data_summary_path']
        self.url_prefix = cfg['data']['url_prefix']

        self.initialize_dirs()

        return


    def initialize_dirs(self):
        ''' intialize some necessary directories'''
        os.makedirs( self.data_dir, exist_ok=True) 
        os.makedirs( self.data_summary_dir, exist_ok=True) 
        return


    def download_monthly_data(  self,
                                states:str=None,
                                start_year:int=None,
                                end_year:int=None):
        ''' download monthly data for specified states
        
        Args: '''
        print(states)
        ### load data for states and months
        for state in states:
            for year in range(start_year, end_year+1):
                for month in range(1,13): 
                    url_address = self.url_prefix +  "_"  + str(year) +  str(month).zfill(2) +"_" + state + "1.csv"
                    os.system( "wget {} -P {}".format(url_address, self.data_dir) )