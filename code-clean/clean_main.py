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
                  'comm pipe - main distance',
                  'comm pipe - commission year',
                  'comm pipe - identification confidence',
                  'comm pipe - leakage',
                  'comm pipe - property pre 1970',
                  'comm pipe - lead pipe ratio',
                  'comm pipe - ar10 lead pipe ratio',
                  'HPI - Average House Price',
                  'HPI - Estimated post 1970 ratio',
                  'replacement - any_replacement',
                  'replacement - success_replacement_count']


# %%
output.to_csv('processed-data/processed_data.csv', float_format="%.5f", index=False)


# %%
