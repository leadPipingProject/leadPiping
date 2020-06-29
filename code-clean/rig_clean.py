
#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

#%% load raw-data/SW - Scottish Water Zonal Phosphate Levels.xls
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

#%% utility functions: convert to relational_data

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


#%% remove empty rows
phosphate_level = remove_empty_row(phosphate_level)

#%% save the headers here (will be removed from the table later)
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


#%% remove headers, and convert to relational table
rig_names, phosphate_level = to_relational(phosphate_level)
phosphate_level.columns = new_header
# 99 rigs

#%% convert types
phosphate_level['Sample Date'] = pd.to_datetime(phosphate_level['Sample Date'])

#%% see sample comments one by one. They are usually relevant.
comments = phosphate_level.loc[np.logical_not(phosphate_level["Sample Comments"].isnull()), :]

#%% remove sample comments
phosphate_level.drop(columns="Sample Comments", inplace=True)

# %% extract zone name

pattern1 = re.compile(r".*-\s*(.*?)\s*[Zz]one.*$")

pattern2 = re.compile(r".*-\s*(.*?)\s*WTW.*$")

pattern3 = re.compile(r".*-\s*(.*?)\s*(\([\w\s]*\))?$")

trailing_pattern1 = re.compile(r"(.*?)/.*$")

trailing_pattern2 = re.compile(r"(.*?)\s+[A-Z]$")

trailing_pattern3 = re.compile(r"(.*?)\s*\(.*\)$")

def remove_trailing_string(s: str):
    matcher1 = re.match(trailing_pattern1, s)
    matcher2 = re.match(trailing_pattern2, s)
    matcher3 = re.match(trailing_pattern3, s)

    if matcher1 is not None:
        return matcher1.group(1)

    if matcher2 is not None:
        return matcher2.group(1)

    if matcher3 is not None:
        return matcher3.group(1)

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


extracted_WOA = [find_zone_name(s) for s in rig_names]
extracted_WOA.sort()

# %%
