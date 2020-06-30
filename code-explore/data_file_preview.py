# preliminary data exploration

# this file contains scripts to load data.

# list of data files:

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
valid_cols = [col for col in lead_sample.columns if col[0:7] != "Unnamed"]
lead_sample = lead_sample[valid_cols]
lead_sample.head()

#%% SW - Comm pipe data.xls
comm_pipe = pd.read_excel("raw-data/SW - Comm pipe data.xls", dtype={"AR10_PROPERTYID":str})
valid_cols = [col for col in comm_pipe.columns if col[0:7] != "Unnamed"]
comm_pipe = comm_pipe[valid_cols]
comm_pipe.head()

#%% SW - Lead Comm Pipe Replacements (2004-2018).csv
pipe_replacement = pd.read_csv("raw-data/SW - Lead Comm Pipe Replacements (2004-2018).csv")
valid_cols = [col for col in pipe_replacement.columns if col[0:7] != "Unnamed"]
pipe_replacement = pipe_replacement[valid_cols]
pipe_replacement.head()

#%% SW - Phosphate Dosing WTWs Y or N
phosphate_dosing = pd.read_excel("raw-data/SW - Phosphate Dosing WTWs Y or N.xlsx")
valid_cols = [col for col in phosphate_dosing.columns if col[0:7] != "Unnamed"]
phosphate_dosing = phosphate_dosing[valid_cols]
phosphate_dosing.head()

#%% SW - Postcodes linked to SW Zonal Structure.xlsb
postcode = pd.read_excel("raw-data/SW - Postcodes linked to SW Zonal Structure.xlsb", engine="pyxlsb")
valid_cols = [col for col in postcode.columns if col[0:7] != "Unnamed"]
postcode = postcode[valid_cols]
postcode.head()

#%% raw-data/SW - Scottish Water Zonal Phosphate Levels.xls
phosphate_level_N = pd.read_excel("raw-data/SW - Scottish Water Zonal Phosphate Levels.xls", sheet_name="North", header=None)
phosphate_level_N.head()
phosphate_level_S = pd.read_excel("raw-data/SW - Scottish Water Zonal Phosphate Levels.xls", sheet_name="South", header=None)
phosphate_level_S.head()
phosphate_level_E = pd.read_excel("raw-data/SW - Scottish Water Zonal Phosphate Levels.xls", sheet_name="East", header=None)
phosphate_level_E.head()
phosphate_level_W = pd.read_excel("raw-data/SW - Scottish Water Zonal Phosphate Levels.xls", sheet_name="West", header=None)
phosphate_level_W.head()

#%% Other - Postcode_ household count_ urban class.csv
household_count = pd.read_csv("raw-data/Other - Postcode_ household count_ urban class.csv")
valid_cols = [col for col in household_count.columns if col[0:7] != "Unnamed"]
household_count = household_count[valid_cols]
household_count.head()

#%% Other - SAA_PropertyAgeData.csv
property_age_data = pd.read_csv("raw-data/Other - SAA_PropertyAgeData.csv", engine="c", encoding="Latin-1")
valid_cols = [col for col in property_age_data.columns if col[0:7] != "Unnamed"]
property_age_data = property_age_data[valid_cols]
property_age_data.head()

#%% Other - UK-HPI-full-file-2019-03.csv
UK_HPI = pd.read_csv("raw-data/Other - UK-HPI-full-file-2019-03.csv")
valid_cols = [col for col in UK_HPI.columns if col[0:7] != "Unnamed"]
UK_HPI = UK_HPI[valid_cols]
UK_HPI.head()

#%%
