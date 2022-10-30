import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

# save data name
DATA = 'KevinRunningStats.csv'
GOAL_PACE = round(6 + 50/60, 3)

# ========================= HELPER FUNCTIONS =====================
# convert pace from string to float (minutes)
def convert_pace(pace_str):
    minutes = int(pace_str.split("'")[0])
    seconds = int(pace_str.split("'")[1])

    return round(float(minutes + seconds/60),2)

# ========================= END HELPER FUNCTIONS =================

# class
class ProgressDashboard:
    # initialize and open csv
    def __init__(self, DATA, GOAL_PACE):
        self.df = pd.read_csv(DATA)
        self.goal_pace = GOAL_PACE

    def clean_data(self):
        """
        Convert pace from minutes and seconds to minutes.
        Filter dataframe to current completed runs and total plan.
        Save a list of the pace columns
        """
        self.filtered_df = self.df[~self.df['Fastest_Mile'].isna()]
        for col in ['Fastest_Mile', 'Slowest_Mile', 'Avg_Pace', 'Goal_Avg_Pace']:
            self.filtered_df['{}_converted'.format(col)] = self.filtered_df[col].apply(convert_pace)
        self.pace_cols = [col for col in self.filtered_df.columns if 'converted' in col]

    def initialize_plots(self):
        self.fig, self.axs = plt.subplots(2,2)
        self.axs = self.axs.ravel()
        self.fig.set_size_inches(20,20)

    # function for plotting progress against total
    def plot_actual(self):
        actual_runs = self.df[~self.df['Fastest_Mile'].isna()]['Miles_Ran'].sum()
        final_distance = self.df['Miles_Ran'].sum()

        g = sns.barplot(x = ['Actual Mileage Ran', 'Total Training Miles'], y = [actual_runs, final_distance], ax = self.axs[0], palette = ['#44BBA4', '#3F88C5'])
        g.bar_label(g.containers[0])
        self.axs[0].set_ylabel('Miles')
        # update legend
        self.axs[0].set_title('Progress Miles versus Total Training Miles')

    # plot pace
    def plot_pace(self):
        # pivot df for graphing
        self.df_m = self.filtered_df.melt(id_vars = ['Date'], value_vars = self.pace_cols, var_name = 'Pace', value_name = 'Minutes Per Mile')

        # define palette
        palette = {'Fastest_Mile_converted' : '#44BBA4',
                    'Slowest_Mile_converted' : '#E94F37',
                    'Avg_Pace_converted' : '#393E41',
                    'Goal_Avg_Pace_converted' : '#3F88C5'}

        g = sns.lineplot(data = self.df_m, x = 'Date', y = 'Minutes Per Mile', hue = 'Pace', ax = self.axs[1], legend = 'full', palette = palette, linewidth = 5)
        self.axs[1].plot([self.df_m['Date'].min(), self.df_m['Date'].max()], [self.goal_pace, self.goal_pace], 'k--')
        self.axs[1].text(sorted(self.df_m['Date'].unique())[-3], 6.5, 'Boston Marathon Qualifying Pace', fontsize = 12)
        self.axs[1].set_ylim(5.5, 9)
        self.axs[1].set_title('Mile Pace Comparison Against Daily Goals')
    
    def plot_scatter(self):
        self.filtered_df['Boston_Qualifying'] = self.filtered_df['Avg_Pace_converted'].apply(lambda pace: 'Qualifying' if pace < self.goal_pace else 'Not Qualifying')
        palette = {'Qualifying' : '#44BBA4',
                    'Not Qualifying' : '#E94F37'}
        g = sns.scatterplot(data = self.filtered_df, x = 'Miles_Ran', y = 'Avg_Pace_converted', hue = 'Boston_Qualifying', ax = self.axs[2], palette = palette, s = 100)
        self.axs[2].set_title('Comparing Miles Ran with Average Mile Pace')
        self.axs[2].set_ylim(5.5, 9)

    def plot_goal_comparison(self):
        self.filtered_df['Seconds_To_Goal'] = self.filtered_df['Avg_Pace_converted'].apply(lambda pace: (pace - self.goal_pace)*60)
        palette = {'Qualifying' : '#44BBA4',
                    'Not Qualifying' : '#E94F37'}
        sns.lineplot(data = self.filtered_df, x = 'Date', y = 'Seconds_To_Goal', ax = self.axs[3], color = '#393E41', linewidth = 3)
        sns.scatterplot(data = self.filtered_df, x = 'Date', y = 'Seconds_To_Goal', hue = 'Boston_Qualifying', ax = self.axs[3], palette = palette, s = 200)
        self.axs[3].set_title('Seconds per Mile to Qualify For Boston Marathon')
        self.axs[3].set_ylim(-120,120)


    def plot(self):
        self.plot_actual()
        self.plot_pace()
        self.plot_scatter()
        self.plot_goal_comparison()
        self.fig.suptitle('Kev\'s LA Marathon Progress Tracker', fontsize = 26)
        plt.show()

def main():
    tracker = ProgressDashboard(DATA, GOAL_PACE)
    tracker.clean_data()
    tracker.initialize_plots()
    tracker.plot()

if __name__ == '__main__':
    main()