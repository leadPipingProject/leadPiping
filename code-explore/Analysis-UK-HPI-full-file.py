#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%% read UK-HPI-full-file
UK_HPI = pd.read_csv("raw-data/Other - UK-HPI-full-file-2019-03.csv")
UK_HPI.iloc[:,0] = pd.to_datetime(UK_HPI.iloc[:,0], format = "%d/%m/%Y")
UK_HPI.head(20)
#%% select first five colums
UK_HPI = UK_HPI.iloc[:, 0:5]
UK_HPI.head(20)
# %% find if every region's collection dates are over one year long
over_one_year = UK_HPI.groupby('RegionName').count()
over_one_year
# %% save result to csv file
over_one_year.to_csv('over_one_year.csv',header = True)

# %%  find the latest date of each region to make sure the date is 01/03/2109
latest_year = UK_HPI[['Date', 'RegionName']].groupby('RegionName').max()

# %% save result to csv file
latest_year.to_csv('latest_year.csv',header = True)

# %% get 12 samples of each RegionName list in time
UK_HPI = UK_HPI.loc[(UK_HPI['Date'] > '2018-03-01'),:]
UK_HPI.head(20)
# %% find the average price of each Region with 2018Code
average_price = UK_HPI.groupby('CouncilArea2018Code').mean()
average_price

# %%
