
#%% import packages and data

###############################################################
# import packages and data
###############################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# load raw-data/SW - Scottish Water Zonal Phosphate Levels.xls
phosphate_level_N = pd.read_excel("raw-data/SW - Scottish Water Zonal Phosphate Levels.xls",
                                  sheet_name="North", header=None, skiprows=[0, 1, 2, 3, 4])
phosphate_level_S = pd.read_excel("raw-data/SW - Scottish Water Zonal Phosphate Levels.xls",
                                  sheet_name="South", header=None, skiprows=[0, 1, 2, 3, 4])
phosphate_level_E = pd.read_excel("raw-data/SW - Scottish Water Zonal Phosphate Levels.xls",
                                  sheet_name="East", header=None, skiprows=[0, 1, 2, 3, 4])
phosphate_level_W = pd.read_excel("raw-data/SW - Scottish Water Zonal Phosphate Levels.xls",
                                  sheet_name="West", header=None, skiprows=[0, 1, 2, 3, 4])
phosphate_level = phosphate_level_N
phosphate_level = phosphate_level.append(phosphate_level_S, ignore_index=True)
phosphate_level = phosphate_level.append(phosphate_level_E, ignore_index=True)
phosphate_level = phosphate_level.append(phosphate_level_W, ignore_index=True)

del phosphate_level_N
del phosphate_level_S
del phosphate_level_E
del phosphate_level_W

phosphate_level = phosphate_level.drop(columns=[8, 9])

#%% convert data to a relational data

###############################################################
# convert data to a relational data
###############################################################

def remove_empty_row(df: pd.DataFrame):
    # we delete all-empty rows
    not_null: np.ndarray = (np.logical_not(df.isnull()).sum(axis=1) > 0)
    not_null_df = df.loc[not_null, :]
    return not_null_df

def to_relational(df: pd.DataFrame):
    to_drop = []
    rig_name: str = None
    new_df = df.reset_index().drop(columns="index")
    rig_names = []

    rig_count = 0

    # put address into the first column
    for row in range(df.shape[0]):
        nonempty_num = np.sum(np.logical_not((new_df.iloc[row, :]).isnull()))

        if nonempty_num == 1:

            # should remove the following rows later
            to_drop += [row, row + 1, row + 2]

            # get the name of rig
            rig_name = new_df.iloc[row, 1]
            rig_names.append(rig_name)
            rig_count += 1

        else:
            new_df.iloc[row, 0] = rig_name

    print("the total number of rigs is : {}".format(rig_count))

    return (rig_names, new_df.drop(to_drop))


# remove empty rows
phosphate_level = remove_empty_row(phosphate_level)

# save the headers here (will be removed from the table later)
header = phosphate_level.iloc[1:3, :]
new_header = ["rig_name"]

def combine(obj1, obj2):
    if str(obj1) == "nan":
        return str(obj2)
    else:
        return str(obj1) + " " + str(obj2)


for i in range(1, header.shape[1]):
    new_header += [combine(header.iloc[0, i], header.iloc[1, i])]

print("new headers: " + str(new_header))


# remove headers, and convert to relational table, add new headers
rig_names, phosphate_level = to_relational(phosphate_level)
phosphate_level.columns = new_header

# convert date
phosphate_level['Sample Date'] = pd.to_datetime(phosphate_level['Sample Date'])

# remove sample comments
phosphate_level.drop(columns="Sample Comments", inplace=True)

#%% extract zone names for linking data

###############################################################
# extract related post-code
###############################################################

pattern1 = re.compile(r".*-\s*(.*?)\s*[Zz]one.*$")

pattern2 = re.compile(r".*-\s*(.*?)\s*WTW.*$")

pattern3 = re.compile(r".*-\s*(.*?)\s*(\([\w\s]*\))?$")

trailing_pattern1 = re.compile(r"(.*?)/.*$")

trailing_pattern2 = re.compile(r"(.*?)\s+[A-Z]$")

trailing_pattern3 = re.compile(r"(.*?)\s+[Bb]ute$")

trailing_pattern4 = re.compile(r"(.*?)\s*\(.*\)$")

def remove_trailing_string(s: str):
    matcher1 = re.match(trailing_pattern1, s)
    matcher2 = re.match(trailing_pattern2, s)
    matcher3 = re.match(trailing_pattern3, s)
    matcher4 = re.match(trailing_pattern4, s)

    if matcher1 is not None:
        return matcher1.group(1)

    if matcher2 is not None:
        return matcher2.group(1)

    if matcher3 is not None:
        return matcher3.group(1)

    if matcher4 is not None:
        return matcher4.group(1)

    return s

def find_zone_name(s: str):
    matcher1 = re.match(pattern1, s)
    matcher2 = re.match(pattern2, s)
    matcher3 = re.match(pattern3, s)

    if matcher1 is not None:
        return remove_trailing_string(matcher1.group(1))

    if matcher2 is not None:
        return remove_trailing_string(matcher2.group(1))

    if matcher3 is not None:
        return remove_trailing_string(matcher3.group(1))

    return None


RIG_NAME_to_WOA_mapper = dict()
for s in rig_names:
    RIG_NAME_to_WOA_mapper[s] = find_zone_name(s)


del pattern1
del pattern2
del pattern3
del trailing_pattern1
del trailing_pattern2
del trailing_pattern3
del trailing_pattern4

# get WOA names from postcode
postcode = pd.read_excel("raw-data/SW - Postcodes linked to SW Zonal Structure.xlsb", engine="pyxlsb")
valid_cols = [col for col in postcode.columns if col[0:7] != "Unnamed"]
postcode = postcode[valid_cols]
WOA_Name = postcode['WOA_Name'].unique()
WOA_Name = WOA_Name[np.logical_not(pd.isnull(WOA_Name))]
WSZ_Name = postcode['WSZ_Name'].unique()
WSZ_Name = WSZ_Name[np.logical_not(pd.isnull(WSZ_Name))]

# find matching WOA_Name
def find_match(str1: str) -> list:
    return_list = []
    for woa in WOA_Name:
        if str1.lower() in woa.lower():
            return_list += [woa]
    return return_list


WOA_mapper = dict()

for woa in set(RIG_NAME_to_WOA_mapper.values()):
    WOA_mapper[woa] = find_match(woa)


# find matching WSZ_Name
def find_match(str1: str) -> list:
    return_list = []
    for wsz in WSZ_Name:
        if str1.lower() in wsz.lower():
            return_list += [wsz]
    return return_list


WSZ_mapper = dict()

for wsz in set(RIG_NAME_to_WOA_mapper.values()):
    WSZ_mapper[wsz] = find_match(wsz)

# final mapper rig_name -> [post_codes]

def get_post_code_from_woa(rig_name: str) -> set:
    return_set: set = set()
    woas: list = WOA_mapper[RIG_NAME_to_WOA_mapper[rig_name]]
    for woa in woas:
        return_set.update(set(postcode.loc[postcode['WOA_Name'] == woa, "Trim Postcode"].to_list()))
    return return_set

def get_post_code_from_wsz(rig_name: str) -> set:
    return_set: set = set()
    wszs: list = WSZ_mapper[RIG_NAME_to_WOA_mapper[rig_name]]
    for wsz in wszs:
        return_set.update(set(postcode.loc[postcode['WSZ_Name'] == wsz, "Trim Postcode"].to_list()))
    return return_set

# REVERSE_POST_CODE_mapper maps from rig_name to post_codes

REVERSE_POST_CODE_mapper = dict()

# initialize
for rig_name in rig_names:
    REVERSE_POST_CODE_mapper[rig_name] = set()

# fill in postcodes
for rig_name in rig_names:
    this_set:set = REVERSE_POST_CODE_mapper[rig_name]
    this_set.update(get_post_code_from_woa(rig_name))
    this_set.update(get_post_code_from_wsz(rig_name))

del postcode

# number of post codes related to each rig
for key, val in REVERSE_POST_CODE_mapper.items():
    print(key + ": " + str(len(val)))




# reverse REVERSE_POST_CODE_mapper and get POST_CODE_mapper
POST_CODE_mapper = dict()
all_post_codes = set()
for v in REVERSE_POST_CODE_mapper.values():
    all_post_codes.update(v)

for p in all_post_codes:
    POST_CODE_mapper[p] = set([k for k, v in REVERSE_POST_CODE_mapper.items() if p in v]);

del RIG_NAME_to_WOA_mapper
del WOA_mapper
del WSZ_mapper
del REVERSE_POST_CODE_mapper

#%% clean extreme values

###############################################################
# Clean extreme values: remove values greater than 20 times
# of rolling median (window = 5)
###############################################################

# remove rows with NA
phosphate_level = phosphate_level[~np.logical_or(pd.isnull(phosphate_level["Lead µgPb/l"]),
                                                 pd.isnull(phosphate_level["Phosphorus µgP/l"]))]


# calculate moving median
phosphate_level.loc[:, 'Lead µgPb/l MVA'] = np.nan
phosphate_level.loc[:, 'Phosphorus µgP/l MVA'] = np.nan

for rig_name in rig_names:

    rolling = phosphate_level.loc[phosphate_level['rig_name'] == rig_name, 'Lead µgPb/l'].rolling(window=5).median()
    phosphate_level.loc[phosphate_level['rig_name'] == rig_name, 'Lead µgPb/l MVA'] = rolling

    rolling = phosphate_level.loc[phosphate_level['rig_name'] == rig_name, 'Phosphorus µgP/l'].rolling(window=5).median()
    phosphate_level.loc[phosphate_level['rig_name'] == rig_name, 'Phosphorus µgP/l MVA'] = rolling

# calculate ratio to moving median
median_ratio_Lead = phosphate_level.loc[:, 'Lead µgPb/l'] / phosphate_level.loc[:, 'Lead µgPb/l MVA']
median_ratio_Phosphorus = phosphate_level.loc[:, 'Phosphorus µgP/l'] / phosphate_level.loc[:, 'Phosphorus µgP/l MVA']

Lead_abnormal = median_ratio_Lead > 20
Phosphorus_abnormal = median_ratio_Phosphorus > 20

# add abnormality flag to dataframe
phosphate_level.loc[:, "Lead_abnormal"] = Lead_abnormal
phosphate_level.loc[:, "Phosphorus_abnormal"] = Phosphorus_abnormal

# visualize abnormal samples
Lead_abnormal_ads = phosphate_level.loc[Lead_abnormal, "rig_name"].unique()
Phosphorus_abnormal_ads = phosphate_level.loc[Phosphorus_abnormal, "rig_name"].unique()

def get_line(rig_name: str, col_name: str):
    return phosphate_level.loc[phosphate_level['rig_name']==rig_name, col_name]

def get_x_points(rig_name: str, col_name: str):
    if_abnormal = phosphate_level[col_name.split(' ')[0] + "_abnormal"]
    return phosphate_level.index[np.logical_and(phosphate_level['rig_name']==rig_name, if_abnormal)]

def get_y_points(rig_name: str, col_name: str):
    if_abnormal = phosphate_level[col_name.split(' ')[0] + "_abnormal"]
    return phosphate_level.loc[np.logical_and(phosphate_level['rig_name']==rig_name, if_abnormal), col_name]

for i in range(Phosphorus_abnormal_ads.shape[0]):
    fig, ax = plt.subplots(1, 1)
    ax.plot(get_line(Phosphorus_abnormal_ads[i], 'Phosphorus µgP/l'))
    ax.scatter(get_x_points(Phosphorus_abnormal_ads[i], 'Phosphorus µgP/l'),
               get_y_points(Phosphorus_abnormal_ads[i], 'Phosphorus µgP/l'))
    plt.plot(get_line(Phosphorus_abnormal_ads[i], 'Phosphorus µgP/l'))
    plt.show()
    plt.close()

for i in range(Lead_abnormal_ads.shape[0]):
    fig, ax = plt.subplots(1, 1)
    ax.plot(get_line(Lead_abnormal_ads[i], 'Lead µgPb/l'))
    ax.scatter(get_x_points(Lead_abnormal_ads[i], 'Lead µgPb/l'), get_y_points(Lead_abnormal_ads[i], 'Lead µgPb/l'))
    plt.plot(get_line(Lead_abnormal_ads[i], 'Lead µgPb/l'))
    plt.show()
    plt.close()

del Lead_abnormal_ads
del Phosphorus_abnormal_ads
del Lead_abnormal
del Phosphorus_abnormal

# remove samples: replace extreme values with NA
phosphate_level.loc[phosphate_level["Lead_abnormal"], 'Lead µgPb/l'] = np.nan
phosphate_level.loc[phosphate_level["Phosphorus_abnormal"], 'Phosphorus µgP/l'] = np.nan

#%% calculate recent means

###############################################################
# calculate recent means for each rig: keep 5 recent non-null records
###############################################################

record_number_Hydrogen = phosphate_level.loc[~phosphate_level['Hydrogen ion pH value'].isnull()]\
    .sort_values(['rig_name', 'Sample Date'], ascending=[True, False])\
    .groupby('rig_name').cumcount()
record_number_Lead = phosphate_level.loc[~phosphate_level['Lead µgPb/l'].isnull()]\
    .sort_values(['rig_name', 'Sample Date'], ascending=[True, False])\
    .groupby('rig_name').cumcount()
record_number_Phosphorus = phosphate_level.loc[~phosphate_level['Phosphorus µgP/l'].isnull()]\
    .sort_values(['rig_name', 'Sample Date'], ascending=[True, False])\
    .groupby('rig_name').cumcount()
record_number_Temperature = phosphate_level.loc[~phosphate_level['Temperature °C'].isnull()]\
    .sort_values(['rig_name', 'Sample Date'], ascending=[True, False])\
    .groupby('rig_name').cumcount()

# take 5 most recent number of records
TAKE_NUM = 5

truncated_Hydrogen = phosphate_level\
    .loc[~phosphate_level['Hydrogen ion pH value'].isnull()][['rig_name', 'Hydrogen ion pH value']]\
        .loc[record_number_Hydrogen < TAKE_NUM, :]
truncated_Lead = phosphate_level\
    .loc[~phosphate_level['Lead µgPb/l'].isnull()][['rig_name', 'Lead µgPb/l']]\
        .loc[record_number_Lead < TAKE_NUM, :]
truncated_Phosphorus = phosphate_level\
    .loc[~phosphate_level['Phosphorus µgP/l'].isnull()][['rig_name', 'Phosphorus µgP/l']]\
        .loc[record_number_Phosphorus < TAKE_NUM, :]
truncated_Temperature = phosphate_level\
    .loc[~phosphate_level['Temperature °C'].isnull()][['rig_name', 'Temperature °C']]\
        .loc[record_number_Temperature < TAKE_NUM, :]


truncated_Hydrogen['Hydrogen ion pH value'] = truncated_Hydrogen['Hydrogen ion pH value'].astype(np.float)
truncated_Lead['Lead µgPb/l'] = truncated_Lead['Lead µgPb/l'].astype(np.float)
truncated_Phosphorus['Phosphorus µgP/l'] = truncated_Phosphorus['Phosphorus µgP/l'].astype(np.float)
truncated_Temperature['Temperature °C'] = truncated_Temperature['Temperature °C'].astype(np.float)

truncated_Hydrogen = truncated_Hydrogen.groupby('rig_name').mean()
truncated_Lead = truncated_Lead.groupby('rig_name').mean()
truncated_Phosphorus = truncated_Phosphorus.groupby('rig_name').mean()
truncated_Temperature = truncated_Temperature.groupby('rig_name').mean()

#%% merge and construct final data at post_code level

###############################################################
# merge and construct final data at post_code level
###############################################################

rig_data: pd.DataFrame = truncated_Hydrogen
rig_data = rig_data.merge(truncated_Lead, left_index=True, right_index=True)
rig_data = rig_data.merge(truncated_Phosphorus, left_index=True, right_index=True)
rig_data = rig_data.merge(truncated_Temperature, left_index=True, right_index=True)

del phosphate_level
del record_number_Hydrogen
del record_number_Lead
del record_number_Phosphorus
del record_number_Temperature
del truncated_Hydrogen
del truncated_Lead
del truncated_Phosphorus
del truncated_Temperature

POST_CODE_RIG_DATA = {"post_code":[],
                      "pH value":[],
                      "Lead µgPb/l":[],
                      "Phosphorus µgP/l":[],
                      "Temperature °C":[]}

progress = 0

for p, v in POST_CODE_mapper.items():
    progress += 1
    data = list(rig_data.loc[np.isin(rig_data.index, list(v)), :].mean(axis=0))
    POST_CODE_RIG_DATA["post_code"].append(p)
    POST_CODE_RIG_DATA["pH value"].append(data[0])
    POST_CODE_RIG_DATA["Lead µgPb/l"].append(data[1])
    POST_CODE_RIG_DATA["Phosphorus µgP/l"].append(data[2])
    POST_CODE_RIG_DATA["Temperature °C"].append(data[3])
    if progress % 1000 == 0:
        print("progress {}/{}, {}%".format(progress, 157678, round(100 * progress / 157678, 2)))

POST_CODE_RIG_DATA = pd.DataFrame(POST_CODE_RIG_DATA)

#%% clean environment
del POST_CODE_mapper
del TAKE_NUM
del WOA_Name
del WSZ_Name
del all_post_codes
del ax
del data
del fig
del header
del i
del key
del median_ratio_Lead
del median_ratio_Phosphorus
del new_header
del p
del progress
del rig_data
del rig_name
del rig_names
del rolling
del s
del this_set
del v
del val
del valid_cols
del woa
del wsz


# %%
