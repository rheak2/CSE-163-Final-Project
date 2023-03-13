"""
This file processes the location data.
Returns a csv file that can be accessed by other files
In separate file as this takes 3 hours to run
"""

import pandas as pd
import numpy as np
import camelot as cm
import os


def first_loc(place):
    """
    modifies location to only contain the first word
    """
    if place != np.nan:
        place = place.split(',')
        place[0] = place[0].strip('"')
        return(place[0])


def process_loc_data():
    # clean up data to match other data
    filename = os.path.join('Table_7_Loc_Data', 'msw3-all.pdf')
    loc = pd.DataFrame()
    next_pages = pd.DataFrame()
    df_2 = pd.DataFrame()
    curr_table = cm.read_pdf(filename, flavor='stream',
                             pages=str(1),
                             table_areas=['230, 3000, 1450, 200'])
    df_1 = curr_table[0].df
    for i in range(2, 107):
        hold_df = pd.DataFrame()
        curr_table = cm.read_pdf(filename, flavor='stream',
                                 pages=str(i),
                                 table_areas=['230, 3000, 1450, 200'])
        hold_df = curr_table[0].df
        next_pages = next_pages.append(hold_df, ignore_index=True)
    for i in range(107, 213):
        hold_df = pd.DataFrame()
        curr_table = cm.read_pdf(filename, flavor='stream',
                                 pages=str(i),
                                 table_areas=['810, 2900, 2000, 300'],
                                 columns=['900, 1036, 1747'])
        hold_df = curr_table[0].df
        df_2 = df_2.append(hold_df, ignore_index=True)
    next_pages['Scientific name'] = next_pages[5] + ' ' + next_pages[6]
    next_pages = next_pages.rename(columns={0: 'ID'})
    next_pages = next_pages[['ID', 'Scientific name']]
    df_1.columns = df_1.iloc[0]
    # drop column names from data
    df_1 = df_1.drop([0])
    df_1['Scientific name'] = df_1['Genus'] + ' ' + df_1['Species']
    df_1 = df_1[['ID', 'Scientific name']]
    df_1 = df_1.append(next_pages)
    # make row 1 the column names
    df_2.columns = df_2.iloc[0]
    # drop column names from data
    df_2 = df_2.drop([0])
    df_2['Location'] = df_2['TypeLocality'].apply(first_loc)
    df_2 = df_2[['ID', 'CommonName', 'Location']]
    loc = pd.merge(pd.merge(df_1, df_2, how='outer'),
                   next_pages, how='outer')
    loc = loc[['Scientific name', 'CommonName', 'Location']]
    loc = loc.rename(columns={'CommonName': 'Common name'})
    loc.to_csv('mammal_location_data.csv')
    loc = loc.dropna()
    return loc


# PROCESS LOC TESTING
# print(process_loc_data())
data = pd.read_csv('mammal_location_data_2.csv')
data = data[['Scientific name', 'Common name', 'Location']]
print(data)
data = data.dropna(thresh=2)
print(data)