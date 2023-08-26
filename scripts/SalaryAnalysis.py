#data analysis
import pandas as pd
import numpy as np
import random as round

#visualization
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

#reading in the data
file_path = "../data/2023StatsAndSalaries.csv"

work = pd.read_csv(file_path)
#creating a copy of the df to manipulate
df = work.copy()

#setting player name as index for readability
df.set_index('Player', inplace=True)

#COLUMN CREATION
df['PPG'] = (df['PTS'] / df['G']).round(1)
df['APG'] = (df['AST'] / df['G']).round(1)
df['TRPG'] = (df['TRB'] / df['G']).round(1)
df['SPG'] = (df['STL'] / df['G']).round(1)
df['BPG'] = (df['BLK'] / df['G']).round(1)
df['astToTO'] = (df['AST'] / df['TOV']).round(1)
df['astToTO'].replace([np.inf], np.nan, inplace=True)
df['dollarPerMinute'] = (df['salary'] / df['MP']).round(2)
df['dollarPerMinute'].replace([np.inf], np.nan, inplace=True)
df['dollarPerFG'] = (df['salary'] / df['FG']).round(2)
df['dollarPerFG'].replace([np.inf], np.nan, inplace=True)
df['dollarPerPoint'] = (df['salary'] / df['PTS']).round(2)
df['dollarPerPoint'].replace([np.inf], np.nan, inplace=True)

minMost = pd.DataFrame(df['dollarPerMinute'].sort_values(ascending=False).round())
minLeast = minMost.iloc[-2::-1] #getting rid of Sterling brown since he scored no points and had NaN value

fgMost = pd.DataFrame(df['dollarPerFG'].sort_values(ascending=False).round())
fgLeast = fgMost.iloc[-3::-1] #getting rid of Sterling brown, and stanley umad since he scored no points and had NaN value

mostPts = pd.DataFrame(df['dollarPerPoint'].sort_values(ascending=False).round(2))
leastPts = mostPts.iloc[-2::-1] #getting rid of Sterling brown since he scored no points and had NaN value


#CORRELATION
salaryCorr = pd.DataFrame()

pgCorr = df[df['Pos'] == 'PG'].corrwith(df['salary'], numeric_only=True).sort_values(ascending=False) #numeric_only=True was what was missing here
pgCorr = pgCorr[1:]

sgCorr = df[df['Pos'] == 'SG'].corrwith(df['salary'], numeric_only=True).sort_values(ascending=False) #numeric_only=True was what was missing here
sgCorr = sgCorr[1:]

sfCorr = df[df['Pos'] == 'SF'].corrwith(df['salary'], numeric_only=True).sort_values(ascending=False) #numeric_only=True was what was missing here
sfCorr = sfCorr[1:]

pfCorr = df[df['Pos'] == 'PF'].corrwith(df['salary'], numeric_only=True).sort_values(ascending=False) #numeric_only=True was what was missing here
pfCorr = pfCorr[1:]

cCorr = df[df['Pos'] == 'C'].corrwith(df['salary'], numeric_only=True).sort_values(ascending=False) #numeric_only=True was what was missing here
cCorr = cCorr[1:]

salaryCorr['PG'] = pgCorr
salaryCorr['SG'] = sgCorr
salaryCorr['SF'] = sfCorr
salaryCorr['PF'] = pfCorr
salaryCorr['C'] = cCorr


#OUTLIER
outliers = df[df['salary'] > df['salary'].mean() + 3 * df['salary'].std()] #could probably make this a query

#ax = sns.histplot(data = df, x='Salary', kde=True, bins = 20).set(title='Dist of Salary')