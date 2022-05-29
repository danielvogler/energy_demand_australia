'''

'''
import os
import sys
import yaml
import glob
import shutil
from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt
from functools import reduce

class DataUtils:

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


    def download_monthly_data(  self,
                                states:str=None,
                                start_year:int=None,
                                end_year:int=None):
        ''' download monthly data for specified states
        
        Args: 
            states [str] = chosen state (e.g. NSW)
            start_year [int] = Year to start download with
            end_year [int] = Year to end download with
        '''

        for state in states:
            for year in range(start_year, end_year+1):
                for month in range(1,13): 
                    url_address = self.url_prefix +  "_"  + str(year) +  str(month).zfill(2) +"_" + state + "1.csv"
                    os.system( "wget {} -P {}".format(url_address, self.data_dir) )
        return


    def merge_monthly_data( self,
                            state:str=None):
        ''' merge monthly energy demand files into one file per state 
        
        Args:
            state [str] = state to merge files for 
        '''
        file_list = sorted( glob.glob( str( self.data_dir / '*{}*.csv'.format(state) ) ) )
        with open( self.data_summary_dir / str( self.data_summary_prefix + state + '.csv') , 'wb') as summary_file:
            for i, file_name in enumerate(file_list):
                    with open(file_name, 'rb') as sub_file:
                        if i != 0:
                            sub_file.readline() 
                        shutil.copyfileobj(sub_file, summary_file)
        return


    def create_df(  self,
                    state:str=None,
                    avg_window:str=None):
        ''' create pandas DF from csv files and process data
        
        Args:
            state [str] = state to pocess data for
            avg_window [str] = window to average over '''

        df = pd.read_csv( self.data_summary_dir / str( self.data_summary_prefix + state + '.csv') )
        df = df.rename( columns={'REGION': 'region', 
                                'SETTLEMENTDATE': 'date', 
                                'TOTALDEMAND': 'total_demand',
                                'RRP': 'rrp',
                                'PERIODTYPE': 'period_type'})
        df['date'] = pd.to_datetime( df['date'] )
        df.to_pickle( self.data_summary_dir / str( self.data_summary_prefix + state + '.pkl') )

        if avg_window:
            df_avg = df.groupby( pd.Grouper(key='date', freq=avg_window) ).mean().reset_index()
            df_avg['region'] = state
            df_avg.to_pickle( self.data_summary_dir / str( self.data_summary_prefix + 'avg_' + state + '.pkl') )
            return df, df_avg
        else:
            return df


    def merge_dfs(  self,
                    name_str:str=None):
        ''' merge all dataframes
        
        Args:
            df_prefix [str] = prefix of file names of df summaries
            name_str [str] = naming string to pass to file name'''

        df_list = []
        for state in self.states:
            df = pd.read_pickle( self.data_summary_dir / str( self.data_summary_prefix + state + '.pkl') )
            df = df.drop(columns=['region'])
            df = df.add_suffix('_' + state)
            df = df.rename( columns={'date_'+state: 'date'})
            df_list.append(df)

        df_all = reduce(lambda  left,right: pd.merge(left,right,on=['date'],
                                            how='outer'), df_list)
        df_all.to_pickle( self.data_summary_dir / str( self.data_summary_prefix + name_str + '_all.pkl') )

        return df_all



    def plot_time_series(   self,
                            df,
                            state):
        ''' plot time series of downloaded data '''

        fig = plt.figure(num=None, figsize=(16, 8), dpi=80, facecolor='w', edgecolor='k')
        font = {'size'   : 14}
        plt.rc('font', **font)
        
        plt.plot(df['date'], df['total_demand'])
        plt.legend(loc='upper center')
        plt.xlabel("Time[-]")
        plt.ylabel("Total demand [-]")
        plt.title("Total demand (" + state + ") over time")
        plt.savefig( self.fig_dir / str( 'total_demand_over_time_' + state + '.png' ), bbox_inches='tight')
        return


    def plot_all_time_series(   self,
                                df):
        ''' plot time series of downloaded data '''

        fig = plt.figure(num=None, figsize=(16, 8), dpi=80, facecolor='w', edgecolor='k')
        font = {'size'   : 14}
        plt.rc('font', **font)
        states = [col for col in df.columns if 'total_demand' in col]

        for state in states:
            plt.plot(df['date'], df[state], label=state)
            plt.legend(loc='upper left')
            plt.xlabel("Time[-]")
            plt.ylabel("Total demand [-]")
            plt.title("Total demand over time")
        plt.savefig( self.fig_dir / str( 'total_demand_over_time_all.png' ), bbox_inches='tight')


        fig = plt.figure(num=None, figsize=(16, 8), dpi=80, facecolor='w', edgecolor='k')
        font = {'size'   : 14}
        plt.rc('font', **font)
        states = [col for col in df.columns if 'rrp' in col]

        for state in states:
            plt.plot(df['date'], df[state], label=state)
            plt.legend(loc='upper left')
            plt.xlabel("Time[-]")
            plt.ylabel("RRP [-]")
            plt.title("RRP over time")
        plt.savefig( self.fig_dir / str( 'rrp_over_time_all.png' ), bbox_inches='tight')
        return