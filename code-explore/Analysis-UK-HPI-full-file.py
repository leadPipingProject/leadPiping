#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%% 
UK_HPI = pd.read_csv("raw-data/Other - UK-HPI-full-file-2019-03.csv", index_col=0, parse_dates=True)
UK_HPI.head(20)
#%% 
UK_HPI = UK_HPI.iloc[:, 0:4]
UK_HPI.head(20)
# %%
over_one_year = UK_HPI.groupby('RegionName').count()

# %%
over_one_year

# %%
over_one_year.to_csv('over_one_year.csv',header = True)

# %%
UK_HPI.reset_index(inplace=True)

# %%
latest_year = UK_HPI[['Date', 'RegionName']].groupby('RegionName').max()

# %%
latest_year.to_csv('latest_year.csv',header = True)

# %%
