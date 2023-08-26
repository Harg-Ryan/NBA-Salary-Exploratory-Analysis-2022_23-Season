#data analysis
import pandas as pd
import numpy as np
import os
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

from IPython.display import HTML, display_html, display


def side_by_side(*dfs):
    '''Prints dataframes side by side in a jupyter notebook.'''
    html = '<div style="display:flex">'
    for df in dfs:
        html += '<div style="margin-right: 2em">'
        html += df.to_html()
        html += '</div>'
    html += '</div>'
    display(HTML(html))

data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
file_path = os.path.join(data_folder, '2023StatsAndSalaries.csv')
work = pd.read_csv(file_path)

#creating a copy of the df to manipulate
df = work.copy()

#setting player name as index for readability
df.set_index('Player', inplace=True)

#COLUMN CREATION
def create_columns(row):
    row['PPG'] = (row['PTS'] / row['G'])
    row['APG'] = (row['AST'] / row['G'])
    row['TRPG'] = (row['TRB'] / row['G'])
    row['SPG'] = (row['STL'] / row['G'])
    row['BPG'] = (row['BLK'] / row['G'])
        
    if row['TOV'] != 0:
        row['astToTO'] = (row['AST'] / row['TOV'])
    else:
        row['TOV'] = np.nan
    return row

df = df.apply(create_columns, axis = 1)
   
# Calculate new columns
df['dollarPerMinute'] = (df['salary'] / df['MP']).round(2)
df['dollarPerFG'] = (df['salary'] / df['FG']).round(2)
df['dollarPerPoint'] = (df['salary'] / df['PTS']).round(2)
    
# Replace infinite values with NaN
df['astToTO'].replace([np.inf, -np.inf], np.nan, inplace=True)
df['dollarPerMinute'].replace([np.inf, -np.inf], np.nan, inplace=True)
df['dollarPerFG'].replace([np.inf, -np.inf], np.nan, inplace=True)
df['dollarPerPoint'].replace([np.inf, -np.inf], np.nan, inplace=True)


#CORRELATION
salaryCorr = pd.DataFrame()

positions = ['PG', 'SG', 'SF', 'PF', 'C']
for position in positions:
    position_corr = df[df['Pos'] == position].corrwith(df['salary'], numeric_only=True).sort_values(ascending=False)[1:]
    salaryCorr[position] = position_corr


#OUTLIER
outliers = df.query('salary > salary.mean() + 3 * salary.std()')

#ax = sns.histplot(data = df, x='Salary', kde=True, bins = 20).set(title='Dist of Salary')