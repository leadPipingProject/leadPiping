#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% SW - Comm pipe data.xls
comm_pipe = pd.read_excel("raw-data/SW - Comm pipe data.xls", dtype={"AR10_PROPERTYID":str})
valid_cols = [col for col in comm_pipe.columns if col[0:7] != "Unnamed"]
comm_pipe = comm_pipe[valid_cols]
