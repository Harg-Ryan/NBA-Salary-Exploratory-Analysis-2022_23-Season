#data analysis
import pandas as pd
import numpy as np
import os
from IPython.display import HTML, display
 

def side_by_side(*dfs):
    '''Prints dataframes side by side in a Jupyter notebook.'''
    html = '<div style="display:flex">'
    for df in dfs:
        html += '<div style="margin-right: 2em">{}</div>'.format(df.to_html())
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
    row['MPG'] = (row['MP'] / row['G'])
    if row['TOV'] != 0:
        row['AST/TO'] = (row['AST'] / row['TOV'])
    else:
        row['TOV'] = np.nan
    return row

df = df.apply(create_columns, axis = 1)
   
# Calculate new columns
df['dollarPerMinute'] = (df['salary'] / df['MP']).round(2)
df['dollarPerFG'] = (df['salary'] / df['FG']).round(2)
df['dollarPerPoint'] = (df['salary'] / df['PTS']).round(2)
    
# Replace infinite values with NaN
inf_cols = ['AST/TO', 'dollarPerMinute', 'dollarPerFG', 'dollarPerPoint']
df[inf_cols] = df[inf_cols].replace([np.inf, -np.inf], np.nan)


#CORRELATION
salaryCorr = pd.DataFrame()

df2 = df.drop(columns=['dollarPerMinute','dollarPerFG', 'dollarPerPoint'], axis=1)
salaryCorr['All'] = df2.corrwith(df2['salary'], numeric_only=True).sort_values(ascending=False)[1:]

positions = ['PG', 'SG', 'SF', 'PF', 'C']
for position in positions:
    position_corr = df[df['Pos'] == position].corrwith(df['salary'], numeric_only=True).sort_values(ascending=False)[1:]
    salaryCorr[position] = position_corr


#OUTLIER
outlier_calc = df['salary'].mean() + 3 * df['salary'].std()
outliers = df.query('salary > @outlier_calc')

#method?
def format_with_commas(value):
    return f'{value:,.2f}'

#age = sa.df['Age'].rank(method='first', ascending= False) creates a rank for the age column and sorts oldest to youngest
#age.loc[['LeBron James']] returns 3, so lebron is the 3rd oldest player in the dataset.
