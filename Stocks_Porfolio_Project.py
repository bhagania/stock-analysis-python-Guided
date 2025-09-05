import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import glob

glob.glob(
    r'/Users/chetanbhagania/Downloads/S&P_resources/individual_stocks_5yr/*.csv')
len(glob.glob(
    '/Users/chetanbhagania/Downloads/S&P_resources/individual_stocks_5yr/*.csv'))

company_list = [r'/Users/chetanbhagania/Downloads/S&P_resources/individual_stocks_5yr/AAPL_data.csv',
                r'/Users/chetanbhagania/Downloads/S&P_resources/individual_stocks_5yr/AMZN_data.csv',
                r'/Users/chetanbhagania/Downloads/S&P_resources/individual_stocks_5yr/GOOG_data.csv',
                r'/Users/chetanbhagania/Downloads/S&P_resources/individual_stocks_5yr/MSFT_data.csv']

df_list = []

for file in company_list:
    current_df = pd.read_csv(file)
    df_list.append(current_df)

all_data = pd.concat(df_list, ignore_index=True)
all_data.isnull().sum()

# Duplicate Record Check
duplicates = all_data.duplicated().sum()
print("Number of duplicate rows:", duplicates)
all_data.dtypes

all_data['date'] = pd.to_datetime(all_data['date'])

# ==============================================================================================
#                   What is the change in price of the stock overtime?
# ==============================================================================================

tech_list = all_data['Name'].unique()

plt.figure(figsize=(20, 12))
for index, company in enumerate(tech_list, 1):
    plt.subplot(2, 2, index)
    filter1 = all_data['Name'] == company
    df = all_data[filter1]
    plt.plot(df['date'], df['close'])
    plt.title(company)

# ==============================================================================================
#                   What is the moving average () of various stocks?
# ==============================================================================================

all_data.head(15)
all_data['close'].rolling(window=10).mean()  # This is moving
new_data = all_data.copy()
ma_day = [10, 20, 50]
for ma in ma_day:
    new_data['close_'+str(ma)] = new_data['close'].rolling(ma).mean()

# Using Pandas Plot
new_data.set_index('date', inplace=True)
new_data.columns

plt.figure(figsize=(20, 15))

for index, company in enumerate(tech_list, 1):
    plt.subplot(2, 2, index)
    filter1 = new_data['Name'] == company
    df = new_data[filter1]
    df[['close_10', 'close_20', 'close_50']].plot(ax=plt.gca())

    plt.title(company)

# ==============================================================================================
#                   What is the %age change of various stocks?
# ==============================================================================================
apple = pd.read_csv(
    r'/Users/chetanbhagania/Downloads/S&P_resources/individual_stocks_5yr/AAPL_data.csv')
# Percentage change between current and prior Value
apple['Daily Return (%)'] = apple['close'].pct_change() * 100

px.line(apple, x='date', y='Daily Return (%)')

# Peaks might be suggesting stock market changes or new product launch!

# ==============================================================================================
#             Performing resampling analysis on apple stocks (yearly,quarterly etc.)
# ==============================================================================================

apple['date'] = pd.to_datetime(apple['date'])
apple.set_index('date', inplace=True)  # Making date as row index

apple['close'].resample('M').mean().plot()  # Monthly
plt.show()

apple['close'].resample('Y').mean().plot()  # Yearly
plt.show()

apple['close'].resample('Q').mean().plot()  # Quarterly
plt.show()

# Concusion: Upward trend regardless of the resampling. Apple is booming.

# ==============================================================================================
#           Check if the closing prices of MSFT, APPL, AMZN & GOOG are correlated or not?
# ==============================================================================================
app = pd.read_csv(company_list[0])
amzn = pd.read_csv(company_list[1])
google = pd.read_csv(company_list[2])
msft = pd.read_csv(company_list[3])

closing_price = pd.DataFrame()
closing_price['apple_close'] = app['close']
closing_price['amzn_close'] = amzn['close']
closing_price['google_close'] = google['close']
closing_price['msft_close'] = msft['close']

sns.pairplot(closing_price)  # Pair Plot of entire DataFrame

'''Between amazon and microsoft, we have a straight line and it shows correlation. 
If closing price of amzn increases then for appl increases as well'''

# Lighter the color, higher the correlation for heatmap below:
sns.heatmap(closing_price.corr(), annot=True)

# ==============================================================================================
#              Whether the daily returns in Stock or closing price are correlated or not?
# ==============================================================================================

(closing_price['apple_close']-closing_price['apple_close'].shift(1)
 )/closing_price['apple_close'].shift(1)*100

for col in closing_price.columns:
    closing_price[col+'_pct_change'] = (closing_price[col] -
                                        closing_price[col].shift(1))/closing_price[col].shift(1) * 100

clsing_p = closing_price[['apple_close_pct_change', 'amzn_close_pct_change',
                          'google_close_pct_change', 'msft_close_pct_change']]

# Graph density chart gives idea where the maximum dataset lies.
g = sns.PairGrid(data=clsing_p)
g.map_diag(sns.histplot)
g.map_lower(sns.scatterplot)
g.map_upper(sns.kdeplot)

clsing_p.corr()

'''From the correlation, if my amzn stck price decreases, 
then there is 40% probability of my MSFT stock price to decrease as well'''
