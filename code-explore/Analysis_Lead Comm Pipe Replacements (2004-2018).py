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

# %%
replacement_finished = replacement_finished.iloc[:, [1,2]]
replacement_finished.head()

# %%
