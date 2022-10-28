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

# convert pace from string to float (minutes)
def convert_pace(pace_str):
    minutes = int(pace_str.split("'")[0])
    seconds = int(pace_str.split("'")[1])

    return round(float(minutes + seconds/60),2)


# function for plotting progress against total
def plot_actual(data):
    actual_runs = data[~data['Fastest_Mile'].isna()]['Miles_Ran'].sum()
    final_distance = data['Miles_Ran'].sum()

    # set up the figure
    fig, axs = plt.subplots(1,1)
    fig.set_size_inches(10,10)

    g = sns.barplot(x = ['Total Distance Ran So Far', 'Goal'], y = [actual_runs, final_distance])
    g.bar_label(g.containers[0])

    plt.show()

# plot pace
def plot_pace(data):
    actual_runs = data[~data['Fastest_Mile'].isna()]
    for col in ['Fastest_Mile', 'Slowest_Mile', 'Avg_Pace', 'Goal_Avg_Pace']:
        actual_runs['{}_converted'.format(col)] = actual_runs[col].apply(convert_pace)

    pace_cols = [col for col in actual_runs.columns if 'converted' in col]

    # pivot df for graphing
    df_m = actual_runs.melt(id_vars = ['Date'], value_vars = pace_cols, var_name = 'Pace', value_name = 'Minutes')
    # set up the figure
    fig, axs = plt.subplots(1,1)
    fig.set_size_inches(10,10)
    print(df_m.head())
    g = sns.lineplot(data = df_m, x = 'Date', y = 'Minutes', hue = 'Pace')
    plt.show()

# plot_actual(running_df)
plot_pace(running_df)