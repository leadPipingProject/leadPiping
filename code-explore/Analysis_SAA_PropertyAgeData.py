#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% read Other - SAA_PropertyAgeData file and change the Postcode to 
property_age_data = pd.read_csv("raw-data/Other - SAA_PropertyAgeData.csv", engine="c", encoding="Latin-1")
property_age_data['Postcode'] = property_age_data['Postcode'].str.replace(' ', '')
property_age_data.head(20)

# %% check the data type of the dataset
property_age_data.info()

# %%  check basic statistic of the float type data
property_age_data.describe()

# %% check the year type and find if their are proper type can be used
property_age_data['Age_Category'].value_counts()
# we nned to find the year post 1970
# Post 1971 is the only one meets the screening criteria

# %% construct a column identify the protery if it is built after 1970
property_age_data['Age_Category'] = property_age_data['Age_Category'].astype('str')
property_age_data['>=1970'] = (property_age_data['Age_Category'] =='AgeCat: Post 1971') | (property_age_data['Age_Year'] >= 1970)
property_age_data.head(20)
# %%calculate the ratio of properties built after 1970 for each Postcode
ratio_of_after_1970 = property_age_data[['>=1970', 'Postcode']].groupby('Postcode').mean()
ratio_of_after_1970
# %%  plot a histogram
max_ratio_of_after_1970 = ratio_of_after_1970['>=1970'].max()
min_ratio_of_after_1970 = ratio_of_after_1970['>=1970'].min()
bins = np.linspace(min_ratio_of_after_1970, max_ratio_of_after_1970, 20)
plt.hist(ratio_of_after_1970['>=1970'], bins)
plt.xlabel('ratio of properties built since 1970 according to each postcode')
plt.ylabel('Number of occurences')
plt.title('Frequency distribution of ratio of properties built since 1970')
plt.show()



# %%
