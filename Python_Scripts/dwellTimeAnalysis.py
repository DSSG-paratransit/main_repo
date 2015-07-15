import numpy as np
import pandas as pd
import statsmodels.api as sm

data = pd.read_csv('D:\\Documents\\Repos\\main_repo\\data\\single_clean_day.csv')
mobaidsOnly = data[pd.notnull(data.MobAids)]
noMobaids = data[pd.isnull(data.MobAids)]


