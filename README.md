# Energy demand forecasting

## Structure
- `config`: Config file containing the chosen settings
- `data_scripts`: Scripts to download, pre-process and save downloaded data
- `model`: Model scripts to perform demand forecasting on the downloaded and processed data

## How-to
1. Adjust desired settings in `/config/config.yaml`
  - `data_download`: `True/False` (download NEM data)
  - `data_preprocess`: `True/False` (Pre-process data, plot data and save results in Pandas dataframes)
  - `start_year`: YYYY (year to start downloads with)
  - `end_year`: YYYY (year to end downloads with)
  - `states`: `NSW/VIC/QLD/SA/TAS` (list all desired states)
  - `avg_window`: `D` (desired averaging window, e.g. 'D' for daily averaging)
2. Run `/data_sripts/data_processing.py` 
   This will download total demand and retail price data for the chosen states and time frame

### Driving factors
There are a number of potential driving factors that influence energy demand and thereby retail price. Among these are:
- Environmental factors:
  - Weather (Temperature extrema and averages)
  - Sunshine hours, sunrise and sunset times, solar flare
- population
- Gas prices
