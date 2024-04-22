import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from scipy.stats import linregress

# File paths
people_file_path = r'C:\Users\kylew\OneDrive\Documents\People.xlsx'
batting_file_path = r'C:\Users\kylew\OneDrive\Documents\Batting.xlsx'

# Read People.xlsx
people_df = pd.read_excel(people_file_path)

# Convert 'debut' column to datetime
people_df['Debut'] = pd.to_datetime(people_df['debut'], format='%Y-%m-%d')

# Filter players with MLB debut dates from 1974 to current year
selected_players = people_df[(people_df['Debut'].dt.year >= 1974) & (people_df['Debut'].dt.year <= datetime.now().year)]

# Read Batting.xlsx
batting_df = pd.read_excel(batting_file_path)

# Merge selected players with batting data
merged_df = pd.merge(selected_players, batting_df, on='playerID', how='inner')

# Calculate age at every year of their career
merged_df['Age'] = merged_df['yearID'] - merged_df['birthYear']
merged_df['Age'] = merged_df['Age'].astype(int)  # Convert age to integer

# Calculate batting average (BA) for each year
merged_df['BA'] = merged_df['H'] / merged_df['AB']

# Calculate On-Base Percentage (OBP)
# OBP = (H + BB + HBP) / (AB + BB + HBP + SF)
merged_df['OBP'] = (merged_df['H'] + merged_df['BB'] + merged_df['HBP']) / (merged_df['AB'] + merged_df['BB'] + merged_df['HBP'] + merged_df['SF'])

# Calculate Slugging Percentage (SLG)
# SLG = ((1B) + (2B x 2) + (3B x 3) + (HR x 4)) / AB
merged_df['1B'] = merged_df['H'] - (merged_df['2B'] + merged_df['3B'] + merged_df['HR'])
merged_df['SLG'] = (merged_df['1B'] + (merged_df['2B'] * 2) + (merged_df['3B'] * 3) + (merged_df['HR'] * 4)) / merged_df['AB']

# Calculate On-Base Plus Slugging (OPS)
merged_df['OPS'] = merged_df['OBP'] + merged_df['SLG']

# Filter out players with less than 200 AB
filtered_df = merged_df[(merged_df['AB'] >= 200)]

# Print playerID, yearID, Age, BA, OPS, SB, and HR
print("PlayerID  |  YearID  |  Age  |  BA  |  OPS  |  SB  |  HR")
print("----------------------------------------------------------")
for index, row in filtered_df.iterrows():
    print(f"{row['playerID']}  |  {row['yearID']}  |  {row['Age']}  |  {row['BA']:.3f}  |  {row['OPS']:.3f}  |  {int(row['SB'])}  |  {row['HR']}")

# Filter age between 20 and 40
filtered_df = filtered_df[(filtered_df['Age'] >= 20) & (filtered_df['Age'] <= 40)]

# Group by age and calculate average OPS, BA, HR, and SB
average_stats_by_age = filtered_df.groupby('Age').agg({'OPS': 'mean', 'BA': 'mean', 'HR': 'mean', 'SB': 'mean'}).reset_index()

# Plotting
plt.figure(figsize=(12, 8))

# Function to plot with line of best fit
def plot_with_line_of_best_fit(ax, x, y, label):
    ax.plot(x, y, marker='o', linestyle='-', label=label)
    slope, intercept, _, _, _ = linregress(x, y)
    ax.plot(x, slope * x + intercept, linestyle='-', color='red')
    ax.set_xticks(np.arange(20, 41, 2))
    ax.grid(True)

# OPS
ax1 = plt.subplot(2, 2, 1)
plot_with_line_of_best_fit(ax1, average_stats_by_age['Age'], average_stats_by_age['OPS'], 'OPS')
ax1.set_ylim([0.720, 0.780])
ax1.set_yticks(np.round(np.arange(0.720, 0.781, 0.010), 3))
plt.xlabel('Age')
plt.ylabel('OPS')
plt.title('OPS Across Age Groups (20-40) Since 1974')
plt.legend()

# BA
ax2 = plt.subplot(2, 2, 2)
plot_with_line_of_best_fit(ax2, average_stats_by_age['Age'], average_stats_by_age['BA'], 'BA')
ax2.set_ylim([0.260, 0.280])
ax2.set_yticks(np.round(np.arange(0.260, 0.281, 0.010), 3))
plt.xlabel('Age')
plt.ylabel('BA')
plt.title('Batting Average Across Age Groups (20-40) Since 1974')
plt.legend()

# HR
ax3 = plt.subplot(2, 2, 3)
plot_with_line_of_best_fit(ax3, average_stats_by_age['Age'], average_stats_by_age['HR'], 'HR')
ax3.set_ylim([8, 14])
ax3.set_yticks(np.arange(8, 15, 1))
plt.xlabel('Age')
plt.ylabel('HR')
plt.title('Home Runs Across Age Groups (20-40) Since 1974')
plt.legend()

# SB
ax4 = plt.subplot(2, 2, 4)
plot_with_line_of_best_fit(ax4, average_stats_by_age['Age'], average_stats_by_age['SB'], 'SB')
ax4.set_ylim([5, 12])
ax4.set_yticks(np.arange(5, 13, 1))
plt.xlabel('Age')
plt.ylabel('SB')
plt.title('Stolen Bases Across Age Groups (20-40) Since 1974')
plt.legend()

plt.tight_layout()
plt.show()

