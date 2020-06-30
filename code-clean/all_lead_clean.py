#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#%% SW - All Lead WQ Samples (2010-18).xls
lead_sample = pd.read_excel("raw-data/SW - All Lead WQ Samples (2010-18).xls")
valid_cols = [col for col in lead_sample.columns if col[0:7] != "Unnamed"]
lead_sample = lead_sample[valid_cols]

#%% clean post-code records
lead_sample['Street Postcode'] = lead_sample['Street Postcode'].str.replace(' ', '')
lead_sample['Street Postcode'] = lead_sample['Street Postcode'].str.upper()

print(lead_sample['Result Status Description'].value_counts())

#%% keep last sample year
lead_sample['Sample Date'] = pd.to_datetime(lead_sample['Sample Date'])
latest_sample_date = lead_sample[['Street Postcode', 'Sample Date']].groupby('Street Postcode').max()
latest_sample_date['Sample Date'] = latest_sample_date['Sample Date'] - pd.DateOffset(years=1)
latest_sample_date.columns = ['Sample Date Offset']
lead_sample = lead_sample.merge(latest_sample_date, left_on='Street Postcode', right_index=True)
lead_sample = lead_sample[lead_sample['Sample Date'] >= lead_sample['Sample Date Offset']]

#%% remove cancelled samples, keep only authorised samples
lead_sample = lead_sample[lead_sample['Result Status Description'] == "Authorised"]


#%% explore samples numbers

# most streets have only one lead sample

(lead_sample['Street Postcode'].value_counts() == 1).value_counts()

#%% aggregate
all_lead_sample = lead_sample[['Street Postcode', 'Result Numeric Entry']].groupby('Street Postcode').mean()

#%% clean up environment
del lead_sample
del latest_sample_date
del valid_cols

#%%
