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
# over_one_year.to_csv('over_one_year.csv',header = True)

# %%  find the latest date of each region to make sure the date is 01/03/2109
latest_year = UK_HPI[['Date', 'RegionName']].groupby('RegionName').max()

# %% save result to csv file
# latest_year.to_csv('latest_year.csv',header = True)

# %% get 12 samples of each RegionName list in time
UK_HPI = UK_HPI.loc[(UK_HPI['Date'] > '2018-03-01'),:]
UK_HPI.head(20)
# %% find the average price of each Region with 2018Code
average_price = UK_HPI.groupby('CouncilArea2018Code').mean()
average_price.reset_index(inplace = True)
average_price.head(20)

# %% read in the file Other - Postcode_ household count_ urban class
# to connect the street postecode from it with CouncilArea2018Code here.
household_count = pd.read_csv("raw-data/Other - Postcode_ household count_ urban class.csv")
household_count['Street postcode'] = household_count['Street postcode'].str.replace(' ', '')
household_count['Street postcode'] = household_count['Street postcode'].str.upper()
household_count.head(20)

# %% merge these two datasets by column CouncilArea2018Code
new_frame = pd.merge(household_count, average_price, left_on = 'CouncilArea2018Code', right_on = 'CouncilArea2018Code', how = 'left')
new_frame = new_frame[['Street postcode', 'AveragePrice']]
new_frame = new_frame[['AveragePrice', 'Street postcode']].groupby('Street postcode').mean()
new_frame.columns=['Average House Price for Street Postcode']
new_frame

# %% exploratory analysis
mean_price_of_all = average_price['AveragePrice'].mean()
#  254893.38524889827
std_of_all = average_price['AveragePrice'].std()
# 134495.95605388767
max_price_of_all = average_price['AveragePrice'].max()
# 1320226.3068333336
min_price_of_all = average_price['AveragePrice'].min()
# 81449.31328916666
median_price_of_all = average_price['AveragePrice'].median()
# 224883.2931166667
bins = np.linspace(min_price_of_all, max_price_of_all, 20)
plt.hist(average_price['AveragePrice'], bins)
plt.xlabel('Number of house price in a range')
plt.ylabel('Number of occurences')
plt.title('Frequency distribution of house price in Scottish Water Region')
plt.show()
# %%
