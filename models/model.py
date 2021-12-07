''' 
'''

import os
import sys
import yaml
from model_utils import ModelUtils

ModelUtils()

df_all = ModelUtils().load_summary_df( str( ModelUtils().data_summary_prefix + 'avg_'), name_str=ModelUtils().avg_window)

print(df_all.head())