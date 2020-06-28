# preliminary data exploration

# SW data files:

# raw-data/SW - All Lead WQ Samples (2010-18).xls
# raw-data/SW - Comm pipe data.xls
# raw-data/SW - Lead Comm Pipe Replacements (2004-2018).csv
# raw-data/SW - Phosphate Dosing WTWs Y or N.xlsx
# raw-data/SW - Postcodes linked to SW Zonal Structure.xlsb
# raw-data/SW - Scottish Water Zonal Phosphate Levels.xls
# Other - Postcode_ household count_ urban class.csv
# Other - SAA_PropertyAgeData.csv
# Other - UK-HPI-full-file-2019-03.csv

#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#%% SW - All Lead WQ Samples (2010-18).xls
lead_sample = pd.read_excel("raw-data/SW - All Lead WQ Samples (2010-18).xls")
lead_sample.head(20)

#%% SW - Comm pipe data.xls
common_pipe = pd.read_excel("raw-data/SW - Comm pipe data.xls")
common_pipe.head(20)

#%% SW - Lead Comm Pipe Replacements (2004-2018).csv
pipe_replacement = pd.read_csv("raw-data/SW - Lead Comm Pipe Replacements (2004-2018).csv")
pipe_replacement.head(20)

#%% SW - Phosphate Dosing WTWs Y or N
phosphate_dosing = pd.read_excel("raw-data/SW - Phosphate Dosing WTWs Y or N.xlsx")
phosphate_dosing.head(20)

#%% SW - Postcodes linked to SW Zonal Structure.xlsb
postcode = pd.read_excel("raw-data/SW - Postcodes linked to SW Zonal Structure.xlsb", engine="pyxlsb")
postcode.head(20)

#%% raw-data/SW - Scottish Water Zonal Phosphate Levels.xls
phosphate_level = pd.read_excel("raw-data/SW - Comm pipe data.xls")
phosphate_level.head(20)

#%% Other - Postcode_ household count_ urban class.csv
household_count = pd.read_csv("raw-data/Other - Postcode_ household count_ urban class.csv")
household_count.head(20)

#%% Other - SAA_PropertyAgeData.csv
property_age_data = pd.read_csv("raw-data/Other - SAA_PropertyAgeData.csv", engine="c", encoding="Latin-1")
property_age_data.head(20)

#%% Other - UK-HPI-full-file-2019-03.csv
UK_HPI = pd.read_csv("raw-data/Other - UK-HPI-full-file-2019-03.csv")
UK_HPI.head(20)

#%%
