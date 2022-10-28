import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

# load data
DATA = 'KevinRunningStats.csv'
running_df = pd.read_csv(DATA)

# view data
print(running_df.head())

