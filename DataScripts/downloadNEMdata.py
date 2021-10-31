# agregate demand data from each of the states
# from https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data

import os
#import system


startyear = 2020  # 1999
endyear = 2021
month = 1

state = "NSW"

states = {"NSW","VIC","QLD","SA","TAS"}

urlPrefix = "https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND"


#urlAddress = "https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_202101_NSW1.csv"


for state in states:
  for year in range(startyear,endyear+1):
    for month in range(1,13): 
      urlAddress = urlPrefix +  "_"  + str(year) +  str(month).zfill(2) +"_" + state + "1.csv"
      os.system('wget ' + urlAddress +" -P Data/")





