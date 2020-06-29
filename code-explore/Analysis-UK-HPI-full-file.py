#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%% read UK-HPI-full-file
UK_HPI = pd.read_csv("raw-data/Other - UK-HPI-full-file-2019-03.csv", index_col=0, parse_dates=True)
UK_HPI.head(20)
#%% select first four colums
UK_HPI = UK_HPI.iloc[:, 0:4]
UK_HPI.head(20)
# %% find if every region's collection dates are over one year long
over_one_year = UK_HPI.groupby('RegionName').count()
over_one_year
# %% save result to csv file
over_one_year.to_csv('over_one_year.csv',header = True)

# %%  find the latest date of each region to make sure the date is 01/03/2109
UK_HPI.reset_index(inplace=True)
latest_year = UK_HPI[['Date', 'RegionName']].groupby('RegionName').max()

# %% save result to csv file
latest_year.to_csv('latest_year.csv',header = True)

# %%
