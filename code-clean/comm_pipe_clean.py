#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

#%% SW - Comm pipe data.xls
comm_pipe = pd.read_excel("raw-data/SW - Comm pipe data.xls", dtype={"AR10_PROPERTYID":str})
valid_cols = [col for col in comm_pipe.columns if col[0:7] != "Unnamed"]
comm_pipe = comm_pipe[valid_cols]

needed_columns = ['AR10_MATERIAL',
                  'Street postcode',
                  'MAIN_DISTANCE',
                  'AGE',
                  'How certain is  the identification?',
                  'Is there any evidence of leakage?',
                  'Is the property age pre 1970?',
                  'Pipe Material ',
                  'Estimated length of pipe in meters']

comm_pipe = comm_pipe[needed_columns]
comm_pipe.columns = ['ar10_Material',
                     'Street postcode',
                     'main distance',
                     'commission year',
                     'identification confidence',
                     'leakage',
                     'property pre 1970',
                     'pipe material',
                     'estimated length of pipe']

comm_pipe['identification confidence'] = comm_pipe['identification confidence'].str.replace(' ', '')
del valid_cols
del needed_columns


#%% convert data to numeric values
print(comm_pipe['ar10_Material'].value_counts())
print(comm_pipe['identification confidence'].value_counts())
print(comm_pipe['leakage'].value_counts())
print(comm_pipe['property pre 1970'].value_counts())
print(comm_pipe['pipe material'].value_counts())


#%% categorical to numerical

# identification confidence to numeric

# 96-100%    6402
# 76-95%     4229
# 51-75%      715
# 95-100%     474
# 75-95%      338
# 50-75%       81
# 0-50%        24
# 50-67%        2

confidence_pattern = re.compile(r'^\d{1,2}-(\d{2,3})%$')

def confidence_to_numeric(s: str) -> int:
    return int(confidence_pattern.match(s).group(1))

comm_pipe['identification confidence'] = [confidence_to_numeric(s) if not pd.isnull(s) else np.nan for s in comm_pipe['identification confidence']]

del confidence_pattern

# is_pipe_lead

# Copper             6180
# Poly               5287
# Lead                866
# LEAD                 28
# copper               18
# PVC                  15
# Other                14
# cast iron             8
# POLY                  7
# Other (Specify)       5
# CI                    1
# asbestos              1
# lead                  1
# Name: pipe material, dtype: int64

comm_pipe['is_pipe_lead'] = np.isin(comm_pipe['pipe material'], ['LEAD', 'Lead', 'lead'])

# ar10_is_pipe_lead

# LEAD      9800
# COPPER    1251
# MDPE      1184
# GI         257
# Lead        29
# Copper      22
comm_pipe['ar10_is_pipe_lead'] = np.isin(comm_pipe['ar10_Material'], ['LEAD', 'Lead', 'lead'])

comm_pipe['leakage'] = np.isin(comm_pipe['leakage'], ['Yes'])

comm_pipe['property pre 1970'] = np.isin(comm_pipe['property pre 1970'], ['Yes', 'yes'])

comm_pipe.drop(columns=['pipe material', 'ar10_Material'])

#%% get final data
comm_pipe = comm_pipe.groupby('Street postcode').mean()


# %%
