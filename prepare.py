'''
prepare functions for the codeup timeseries exercises
'''

import pandas as pd

def prep_heb_data(df):
    '''
    Takes in the df of combined items, sales, and stores info.
    - Converts index to datetime formatted sale date
    - adds columns for month and day of the week
    - adds a sales total column (sale_amount * item_price)
    '''
    # if no time of day information is stored (i.e. all times == 00:00:00)
    if df.sale_date.str.endswith(' 00:00:00 GMT').mean() == 1:
        # then we will truncate the sale_date string for faster processing to_datetime
        df['sale_date'] = df.sale_date.str[:-13]
        # convert the sale_date to a pandas datetime with format specifier
        df['sale_date'] = pd.to_datetime(df.sale_date, format='%a, %d %b %Y')
    else:
        # convert the sale_date to pandas datetime
        df['sale_date'] = pd.to_datetime(df.sale_date) 
    # set sale_date as the index
    df = df.set_index('sale_date').sort_index()
    # add month column
    df['month'] = df.index.strftime('%m-%b')
    # add weekday column
    df['weekday'] = df.index.strftime('%w-%a')
    # add sales_total column
    df['sales_total'] = df.sale_amount * df.item_price
    
    return df

def prep_opsd_germany_data(df):

    # rename columns for convenience
    for col in df.columns:
        df = df.rename(columns={col: col.lower().replace('+', '_')})
    # convert the date column to a datetime type
    df['date'] = pd.to_datetime(df.date)
    # set the index to the date column and sort
    df = df.set_index('date').sort_index()
    # add month and year columns
    df['month'] = df.index.strftime('%m-%b')
    df['year'] = df.index.year
    # fill missing values
    df['wind'] = df.wind.fillna(0)
    df['solar'] = df.solar.fillna(0)
    df['wind_solar'] = df.wind + df.solar

    return df