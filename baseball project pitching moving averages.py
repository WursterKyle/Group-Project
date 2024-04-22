import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# File paths
people_file_path = r'C:\Users\kylew\OneDrive\Documents\People.xlsx'
pitching_file_path = r'C:\Users\kylew\OneDrive\Documents\Pitching.xlsx'

# Step 1: Read People.xlsx
people_df = pd.read_excel(people_file_path)

# Convert 'debut' column to datetime
people_df['debut'] = pd.to_datetime(people_df['debut'])

# Filter players with MLB debut dates from 1974 to current year and age between 22 and 36
selected_players = people_df[(people_df['debut'].dt.year >= 1974) & 
                             (people_df['debut'].dt.year <= pd.Timestamp.now().year) &
                             (people_df['birthYear'] <= pd.Timestamp.now().year - 22) &
                             (people_df['birthYear'] >= pd.Timestamp.now().year - 37)]

# Step 2: Read Pitching.xlsx
pitching_df = pd.read_excel(pitching_file_path)

# Merge selected players with pitching data
merged_df = pd.merge(selected_players, pitching_df, on='playerID', how='inner')

# Calculate age at every year of their career
merged_df['Age'] = merged_df['yearID'] - merged_df['birthYear']
merged_df['Age'] = merged_df['Age'].astype(int)  # Convert age to integer

# Calculate IP
merged_df['IP'] = merged_df['IPouts'] / 3

# Calculate WHIP and round to two decimal places
merged_df['WHIP'] = ((merged_df['H'] + merged_df['BB']) / merged_df['IP']).round(2)

# Filter out players with ages between 22 and 36 and less than 50 IP
filtered_df = merged_df[(merged_df['Age'] >= 22) & (merged_df['Age'] <= 36) & (merged_df['IP'] >= 50)]

# Step 3: Print playerID, yearID, Age, WHIP, and ERA for each player
for index, row in filtered_df.iterrows():
    print(f"PlayerID: {row['playerID']}, Year: {row['yearID']}, Age: {row['Age']}, WHIP: {row['WHIP']}, ERA: {row['ERA']}")

# Step 4: Filter out players with ages between 22 and 36 and less than 50 IP (Already done in Step 2)

# Step 5: Create a graph for ERA across age groups since 1974 with a line of best fit
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
age_era_avg = filtered_df.groupby('Age')['ERA'].mean()
plt.plot(age_era_avg.index, age_era_avg.values, marker='o', label='Average ERA')
slope, intercept, r_value, _, _ = linregress(age_era_avg[age_era_avg.index != 36].index, age_era_avg[age_era_avg.index != 36].values)
plt.plot(age_era_avg.index, intercept + slope * age_era_avg.index, 'r')
plt.text(22, 4.45, f'R^2 = {r_value**2:.2f}', color='blue')
plt.xlabel('Age')
plt.ylabel('ERA')
plt.title('ERA Across Age Groups (22-36) Since 1974')
plt.xticks(np.arange(22, 38, 2))  # Set x-axis ticks from 22 to 36 increasing by 2
plt.yticks(np.arange(3.50, 4.51, 0.10))  # Set y-axis ticks from 3.50 to 4.50 increasing by 0.10
plt.gca().yaxis.set_major_formatter('{:.2f}'.format)  # Format y-axis to two decimal places

# Step 6: Create a graph for WHIP across age groups since 1974 with a line of best fit
plt.subplot(1, 2, 2)
age_whip_avg = filtered_df.groupby('Age')['WHIP'].mean()
plt.plot(age_whip_avg.index, age_whip_avg.values, marker='o', label='Average WHIP')
slope, intercept, r_value, _, _ = linregress(age_whip_avg[age_whip_avg.index != 36].index, age_whip_avg[age_whip_avg.index != 36].values)
plt.plot(age_whip_avg.index, intercept + slope * age_whip_avg.index, 'r')
plt.text(22, 1.45, f'R^2 = {r_value**2:.2f}', color='blue')
plt.xlabel('Age')
plt.ylabel('WHIP')
plt.title('WHIP Across Age Groups (22-36) Since 1974')
plt.xticks(np.arange(22, 38, 2))  # Set x-axis ticks from 22 to 36 increasing by 2
plt.yticks(np.arange(1.00, 1.51, 0.10))  # Set y-axis ticks from 1.00 to 1.50 increasing by 0.10
plt.gca().yaxis.set_major_formatter('{:.2f}'.format)  # Format y-axis to two decimal places

plt.tight_layout()
plt.show()
