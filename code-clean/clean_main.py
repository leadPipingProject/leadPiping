#%% run the scripts

print("Running: code-clean/all_lead_clean.py")
exec(open("code-clean/all_lead_clean.py").read())


print("Running: code-clean/comm_pipe_clean.py")
exec(open("code-clean/comm_pipe_clean.py").read())


print("Running: code-clean/pipe_replacement_clean.py")
exec(open("code-clean/pipe_replacement_clean.py").read())


print("Running: code-clean/property_age_clean.py")
exec(open("code-clean/property_age_clean.py").read())


print("Running: code-clean/rig_clean.py")
exec(open("code-clean/rig_clean.py").read())


print("Running: code-clean/UK_HPI_clean.py")
exec(open("code-clean/UK_HPI_clean.py").read())


#%%
POST_CODE_RIG_DATA.head()
#%%
all_lead_sample.head()
#%%
comm_pipe.head()
#%%
property_price.head()
#%%
ratio_of_after_1970.head()
#%%
replacement_finished.head()

#%%
postcode = pd.read_excel("raw-data/SW - Postcodes linked to SW Zonal Structure.xlsb", engine="pyxlsb")
POST_CODE_RIG_DATA.set_index('post_code', inplace = True)


#%% merge data
output = postcode[['Trim Postcode']]
output.columns = ["post_code"]

#%%

output = output.merge(POST_CODE_RIG_DATA, left_on='post_code', right_index=True, how='left')
output = output.merge(all_lead_sample, left_on='post_code', right_index=True, how='left')
output = output.merge(comm_pipe, left_on='post_code', right_index=True, how='left')
output = output.merge(property_price, left_on='post_code', right_index=True, how='left')
output = output.merge(ratio_of_after_1970, left_on='post_code', right_index=True, how='left')
output = output.merge(replacement_finished, left_on='post_code', right_index=True, how='left')

#%%
output.columns = ['post_code',
                  'rig - PH value',
                  'rig - Lead µgPb/l',
                  'rig - Phosphorus µgP/l',
                  'rig - Temperature °C',
                  'sample - lead µgPb/l',
                  'comm pip - main distance',
                  'comm pip - commission year',
                  'comm pip - identification confidence',
                  'comm pip - leakage',
                  'comm pip - property pre 1970',
                  'comm pip - lead pip ratio',
                  'comm pip - ar10 lead pip ratio',
                  'HPI - Average House Price',
                  'HPI - Estimated post 1970 tatio',
                  'replacement - any_replacement',
                  'replacement - success_replacement_count']


# %%
output.to_csv('processed-data/procseed_data.csv', float_format="%.5f")


# %%
