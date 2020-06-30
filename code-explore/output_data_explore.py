#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%%
output = pd.read_csv('processed-data/processed_data.csv')


# %%
output.head()

# %%
fig, ax = plt.subplots(1, 1)
sns.distplot(np.log(output['rig - Lead µgPb/l']), ax=ax)
sns.distplot(np.log(output['sample - lead µgPb/l']), ax=ax)
plt.show()

#%%
plt.scatter(np.log(output['rig - Lead µgPb/l']),
            np.log(output['sample - lead µgPb/l']), alpha=0.1)

# %%
