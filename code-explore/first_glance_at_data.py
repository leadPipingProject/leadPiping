# preliminary data exploration

# all data files:

# raw-data/Other - Postcode_ household count_ urban class.csv 
# raw-data/Other - SAA_PropertyAgeData.csv                    
# raw-data/Other - UK-HPI-full-file-2019-03.csv               
# raw-data/SW - All Lead WQ Samples (2010-18).xls             
# raw-data/SW - Comm pipe data.xls
# raw-data/SW - Lead Comm Pipe Replacements (2004-2018).csv
# raw-data/SW - Phosphate Dosing WTWs Y or N.xlsx
# raw-data/SW - Postcodes linked to SW Zonal Structure.xlsb
# raw-data/SW - Scottish Water Zonal Phosphate Levels.xls

#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% SW - Postcodes linked to SW Zonal Structure.xlsb
pipe_replacement = pd.read_csv("raw-data/SW - Lead Comm Pipe Replacements (2004-2018).csv")
pipe_replacement.head()

#%% SW - Phosphate Dosing WTWs Y or N
phosphate_dosing = pd.read_excel("raw-data/SW - Phosphate Dosing WTWs Y or N.xlsx")
phosphate_dosing.head()

#%% SW - Postcodes linked to SW Zonal Structure.xlsb
postcode = pd.read_excel("raw-data/SW - Postcodes linked to SW Zonal Structure.xlsb", engine="pyxlsb")
postcode.head()

#%% SW - All Lead WQ Samples (2010-18).xls
lead_sample = pd.read_excel("raw-data/SW - All Lead WQ Samples (2010-18).xls")
lead_sample.head()

#%% SW - Comm pipe data.xls
common_pipe = pd.read_excel("raw-data/SW - Comm pipe data.xls")
common_pipe.head()

#%% raw-data/SW - Scottish Water Zonal Phosphate Levels.xls
phosphate_level = pd.read_excel("raw-data/SW - Comm pipe data.xls")
phosphate_level.head()

#%%