#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% read in file SW - Lead Comm Pipe Replacements (2004-2018).csv
pipe_replacement = pd.read_csv("raw-data/SW - Lead Comm Pipe Replacements (2004-2018).csv")
valid_cols = [col for col in pipe_replacement.columns if col[0:7] != "Unnamed"]
pipe_replacement = pipe_replacement[valid_cols]
pipe_replacement.head()


# %% check the data type of the dataset
pipe_replacement.info()
# and here we find the WO Completed Status has a little null vlaues
# we may need to drop them

# %%  check basic statistic of the float type data
pipe_replacement.describe()


# %%  chose features we need to build a new dataset and makesure all postcode are capitalized and no ' '
pipe_replacement = pipe_replacement[['WO Completed Status', 'WO Create Date', 'Street postcode']]
pipe_replacement['Street postcode'] = pipe_replacement['Street postcode'].str.replace(' ', '')
pipe_replacement['Street postcode'] = pipe_replacement['Street postcode'].str.upper()
pipe_replacement.head(20)

# %% find if the replacement date are all after 1970
# we need to change the datetype and make a Boolean slice
pipe_replacement['WO Create Date'] = pd.to_datetime(pipe_replacement['WO Create Date'])
pipe_replacement = pipe_replacement.loc[pipe_replacement['WO Create Date'] >= '1970-01-01',:]
pipe_replacement.info()
# <class 'pandas.core.frame.DataFrame'>
# Int64Index: 12472 entries, 0 to 12471
# Data columns (total 3 columns):
#  #   Column               Non-Null Count  Dtype         
# ---  ------               --------------  -----         
#  0   WO Completed Status  12331 non-null  object        
#  1   WO Create Date       12472 non-null  datetime64[ns]
#  2   Street postcode      12472 non-null  object        
# dtypes: datetime64[ns](1), object(2)
# Here we find that all the replacement date are after 1970
# so we can use all the sample data

# %% find the class types of feature WO Completed Status
pipe_replacement['WO Completed Status'].value_counts()
# All Complete                                          5249
# All Complete with Comments                            4670
# Complete (Partial)                                    1434
# Cancelled with comments                                664
# Bulk Closure                                           294
# Cancelled by Bulk Closure                               18
# System Closure                                           2
# Here we find the classes of this feature and the complete status 
# are mainly two types: All Complete and All Complete with Comments 
# so we need to generate a column that records the street postcode with
# whether its pipe has been finished replacement


# %% here we generate the column that records the street postcode with
# whether its pipe has been finished replacement
# we name it as replacement_finished
# here we find the elements in WO Completed Status have lots of meaningless blanks and we need to delete them
pipe_replacement['WO Completed Status'] = pipe_replacement['WO Completed Status'].astype('str')
pipe_replacement['WO Completed Status'] = pipe_replacement['WO Completed Status'].str.strip()
pipe_replacement['replacement_finished'] = (pipe_replacement['WO Completed Status'] == 'All Complete') | (pipe_replacement['WO Completed Status'] == 'All Complete with Comments')
pipe_replacement.head()

# %% check status of replacement
pipe_replacement['replacement_finished'].value_counts()
# True     9919
# False    2553

# %% caculate the ratio of the replacement finished for each street postcode
replacement_finished = pipe_replacement[['replacement_finished', 'Street postcode']].groupby('Street postcode').mean()
replacement_finished.columns = ['replacement_finished_ratio']
replacement_finished['any_replacement'] = replacement_finished['replacement_finished_ratio'] == 1.0
replacement_count = pipe_replacement[['replacement_finished', 'Street postcode']].groupby('Street postcode').count()
replacement_finished['success_replacement_count'] = replacement_count['replacement_finished'] * replacement_finished['replacement_finished_ratio']
replacement_finished.head(20)

# %% only need last two column
replacement_finished = replacement_finished.iloc[:, [1,2]]
replacement_finished.head()

# %% however, the postcode in the above dataset for Scottish Water are not complete
# we need to use another dataset called SW - Postcodes linked to SW Zonal Structure
# to find the complete postcode and merge them together
postcode = pd.read_excel("raw-data/SW - Postcodes linked to SW Zonal Structure.xlsb", engine="pyxlsb")
valid_cols = [col for col in postcode.columns if col[0:7] != "Unnamed"]
postcode = postcode[valid_cols]
postcode = postcode.iloc[:,0:2]
postcode.columns = ['Street postcode','District postcode']
postcode.head()

# %%  delete the nan value sample points and standardize the postcode format
postcode = postcode.dropna()
postcode['Street postcode'] = postcode['Street postcode'].str.replace(' ', '')
postcode['Street postcode'] = postcode['Street postcode'].str.upper()

# %% merging
replacement_finished = pd.merge(postcode, replacement_finished, left_on = 'Street postcode', right_on = 'Street postcode', how = 'left')


# %%  view information
replacement_finished.info()
# <class 'pandas.core.frame.DataFrame'>
# Int64Index: 173319 entries, 0 to 173318
# Data columns (total 4 columns):
#  #   Column                     Non-Null Count   Dtype  
# ---  ------                     --------------   -----  
#  0   Street postcode            173319 non-null  object 
#  1   District Postcode          173319 non-null  object 
#  2   any_replacement            7984 non-null    object 
#  3   success_replacement_count  7984 non-null    float64
# dtypes: float64(1), object(3)
replacement_finished.head(20)
# %%  For any_replacement replace the NAN value with False
# For success_replacement_count replace the NAN value with 0
# and we only use Street postcode any_replacement and success_replacement_count
replacement_finished['success_replacement_count'].fillna(0, inplace = True)
replacement_finished['any_replacement'].fillna(False, inplace = True)
replacement_finished.set_index('Street postcode', inplace = True)
replacement_finished = replacement_finished.iloc[:,1:3]
replacement_finished.head(20)

# %%  plot a histogram
replacement_finished['success_replacement_count'].value_counts()
# 0.0     165767
# 1.0       5724
# 2.0       1288
# 3.0        352
# 4.0        100
# 5.0         55
# 6.0         19
# 7.0          4
# 8.0          4
# 9.0          3
# 15.0         1
# 14.0         1
# 10.0         1
# Name: success_replacement_count, dtype: int64

# %%  plot a histogram
max_replacement_finished = replacement_finished['success_replacement_count'].max()
min_replacement_finished = replacement_finished['success_replacement_count'].min()
bins = np.linspace(min_replacement_finished, max_replacement_finished, 15)
plt.hist(replacement_finished['success_replacement_count'], bins)
plt.xlabel('number counts of success replacement of the pipes for Scottich Water')
plt.ylabel('Number of occurences')
plt.title('Frequency distribution of number counts of success replacement')
plt.show()


# %% delete non useful variables
del bins
del max_replacement_finished
del min_replacement_finished
del pipe_replacement
del postcode
del replacement_count
del valid_cols


# %%
replacement_finished.head(20)

# %%
