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
    print('running process loc data')
    # clean up data to match other data
    filename = os.path.join('Table_7_Loc_Data', 'msw3-all-2.pdf')
    loc = pd.DataFrame()
    next_pages = pd.DataFrame()
    df_2 = pd.DataFrame()
    curr_table = cm.read_pdf(filename, flavor='stream',
                             pages=str(1),
                             table_areas=['230, 3000, 1450, 200'])
    df_1 = curr_table[0].df
    print(df_1)
    for i in range(2, 10):
        hold_df = pd.DataFrame()
        print('running 1 ' + str(i))
        curr_table = cm.read_pdf(filename, flavor='stream',
                                 pages=str(i),
                                 table_areas=['230, 3000, 1450, 200'])
        hold_df = curr_table[0].df
        next_pages = next_pages.append(hold_df, ignore_index=True)
    print(next_pages)
    for i in range(107, 116):
        hold_df = pd.DataFrame()
        print('running 2 ' + str(i))
        curr_table = cm.read_pdf(filename, flavor='stream',
                                 pages=str(i),
                                 table_areas=['810, 2900, 2000, 300'],
                                 columns=['900, 1036, 1747'])
        hold_df = curr_table[0].df
        df_2 = df_2.append(hold_df, ignore_index=True)
    print('done with loops')
    # drop the extra info on top, make row 1 the column names
    next_pages['Scientific name'] = next_pages[5] + ' ' + next_pages[6]
    next_pages = next_pages.rename(columns={0: 'ID'})
    next_pages = next_pages[['ID', 'Scientific name']]
    # print(df_1)
    df_1.columns = df_1.iloc[0]
    # drop column names from data
    df_1 = df_1.drop([0])
    df_1['Scientific name'] = df_1['Genus'] + ' ' + df_1['Species']
    df_1 = df_1[['ID', 'Scientific name']]
    df_1 = df_1.append(next_pages)
    # print(df_1)
    # print(df_1.columns)
    # print(df_2)
    # make row 1 the column names
    df_2.columns = df_2.iloc[0]
    # drop column names from data
    df_2 = df_2.drop([0])
    print(df_2.columns)
    df_2['Location'] = df_2['TypeLocality'].apply(first_loc)
    df_2 = df_2[['ID', 'CommonName', 'Location']]
    # print(df_2['CommonName'])
    # print('df 1')
    # print(df_1)
    loc = pd.merge(pd.merge(df_1, df_2, how='outer'),
                   next_pages, how='outer')
    print(loc)
    loc = loc[['Scientific name', 'CommonName', 'Location']]
    print(loc.columns)
    loc = loc.rename(columns={'CommonName': 'Common name'})
    next_pages.to_csv('checking_1.2.csv')
    df_1.to_csv('checking_part_1.csv')
    df_2.to_csv('checking part_2.csv')
    loc.to_csv('mammal_location_data.csv')
    loc = loc.dropna()
    return loc
    # print(loc)


# PROCESS LOC TESTING
# print(process_loc_data())
# test = cm.read_pdf('Table_7_Loc_Data/msw3-all-2.pdf', flavor='stream',
#                    pages=str(4),
#                    table_areas=['230, 3000, 1450, 200'])
# test = test[0].df
# test.to_csv('test.csv')
