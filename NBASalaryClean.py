# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24, 2023

@author: Ryan

This is the script for creating and cleaning the dataset for the NBA Salary Analysis.
No columns are added in this process, I only removed or replaced dirty data (dupes, etc)

Players were dropped from the dataframe if their salary entry was empty,
verified that these values were unavailble, not just missing or incomplete on data transfer

Positional mapping conversion was determined by which position the player had played
the most games at according to their player page on basketball-reference.com for
simplification purposes.
"""
import pandas as pd
import numpy as np
import logging
import sys  # Import the sys module for console output


# Configure logging to display only INFO level messages in the console
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
#load data
totals = pd.read_csv(r'C:\Users\Ryan\Documents\GitHub\NBA-Salary-Exploratory-Analysis-2022_23-Season\2023totals.csv')
salaries = pd.read_csv(r'C:\Users\Ryan\Documents\GitHub\NBA-Salary-Exploratory-Analysis-2022_23-Season\2023salaries.csv')

#log checks
logging.info("Columns in 'totals': %s", totals.columns)
logging.info("Columns in 'salaries': %s", salaries.columns)


# Rename columns for consistency and clarity
totals.rename(columns={'Player-additional': 'PlayerID'}, inplace=True)
salaries.rename(columns={'-9999': 'PlayerID', '2022-23': 'salary'}, inplace=True)

# Remove unnecessary columns from both dataframes
totals.drop(['Rk'], axis=1, inplace=True)
salaries.drop(['Rk', 'Tm', 'Player', '2023-24', '2024-25', '2025-26', '2026-27',
              '2027-28', 'Guaranteed'], axis=1, inplace=True)

# Remove duplicated rows from the salaries dataframe
salaries = salaries.drop_duplicates(keep='first')

# Convert 'Pos' and 'Tm' columns to categorical data types
totals['Pos'] = totals['Pos'].astype('category')
totals['Tm'] = totals['Tm'].astype('category')

# Remove '$' from salary values and convert to integer data type, fill nan with -1 for later inspection
salaries['salary'] = salaries['salary'].str.replace('$', '')
salaries['salary'] = salaries['salary'].fillna(-1)
salaries['salary'] = salaries['salary'].astype(np.int64)

# Combine data from both dataframes based on 'pid'
combined = pd.merge(totals, salaries, on='PlayerID', how='inner')

#giving merged df entries that had no salary entry a value so the column can be converted.
combined['salary'] = combined['salary'].fillna(-1)
combined['salary'] = combined['salary'].astype(np.int64)

# Drop rows where salary is -1 (players without salaries)
combined.drop(combined[combined['salary'] == -1].index, inplace=True)

#checking to see if any entries aren't 1 of the 5 positions.
filtered_rows = combined[~combined['Pos'].isin(['PG', 'SG', 'SF', 'PF', 'C'])]
result = filtered_rows
logging.info(filtered_rows)

# Map hybrid positions to primary positions
position_mapping = {
    'SG-PG': 'SG',
    'SF-SG': 'SF',
    'PF-SF': 'PF'}
combined['Pos'] = combined['Pos'].replace(position_mapping)

#changing TJ to a SF since he's the only player that was different in the mapping
combined.loc[combined['Player'] == 'T.J. Warren', 'Pos'] = 'SF'

#ensuring there's only 5 positions now.
logging.info(combined['Pos'].value_counts())

combined.to_csv('2023StatsAndSalaries.csv', index=False)