import camelot as cm
import pandas as pd
import os
import numpy as np
from operator import itemgetter


CLASSES_1 = ['INVERTEBRATES', 'REPTILES', 'BIRDS', 'PLANTS',
             'FUNGI', 'FISHES', 'ORCHIDS', 'LEGUMES', 'AMPHIBIANS',
             'MOLLUSCS', 'CORALS', 'CRUSTACEANS', 'GRASSHOPPERS & CRICKETS'
             'LEPIDOPTERA', 'TREES', 'OTHER FLOWERING PLANTS', 'BEETLES',
             'HYMENOPTERA', 'ODONATA', 'OTHER INVERTEBRATES', 'CONIFERS',
             'MAGNOLIAS', 'DRAGONFLIES & DAMSELFLIES', 'CRABS & CRAYFISHES',
             'HORSESHOE CRABS', 'FERNS', 'BONY FISHES', 'SHARKS & RAYS',
             'LAMPREYS', 'MOTHS & BUTTERFLIES', 'GRASSHOPPERS',
             '"LAMPREYS, etc."', '"GRASSHOPPERS, LOCUSTS & CRICKETS"',
             'FRESHWATER SHRIMPS', '"BUTTERFLIES, MOTHS"',
             '"DRAGONFLIES, DAMSELFLIES"', 'MOSSES', 'FERNS & ALLIES',
             'BUTTERFLIES', 'BUTTERFLIES & MOTHS',
             '"CRAYFISHES, CRABS, LOBSERS, etc"', 'FERNS & allies',
             'CYCADS', 'MAMMALS']

CLASSES_2 = ['MAMMALS (Mammalia)', 'BIRDS (Aves)', 'REPTILES (Reptilia)',
             'AMPHIBIANS (Amphibia)', 'BONY FISHES (Actinopterygii)',
             'SHARKS & RAYS (Chondrichthyes)',
             'BUTTERFLIES & MOTHS (Insecta: Lepidoptera)',
             'DRAGONFLIES & DAMSELFLIES (Insecta: Odonata)',
             'MANTISES (Insecta: Mantodea)',
             '"CRUSTACEANS (Arthropoda: Branchiopoda, Cephalocardia,'
             'Malacostraca, Maxillopoda, Ostracoda, and Remipedia)"',
             'MOLLUSCS (Mollusca)',
             'FLOWERING PLANTS (Liliopsida and Magnoliopsida)',
             '"FERNS (Marattiopsida, Polypodiopsida and Psilotopsida)"',
             'MILLIPEDES (Diplopoda)', 'FUNGI (Mushrooms and Lichens)']


def first_loc(place):
    """
    modifies location to only contain the first word
    """
    if place != np.nan:
        place = place.split(',')
        return(place[0])


def update_threat(df, year_1, year_2):
    cy = 'List (' + str(year_2) + ')'
    py = 'List (' + str(year_1) + ')'
    if year_2 != 2007:
        df[cy] = df[cy].where(df[cy] != 'nan', df[py])
        return(df[cy])
    else:
        nt = ['NT'] * len(df[cy])
        df[cy] = df[cy].where(df[cy] != 'nan', nt)
        return(df[cy])


def fill_in_threat(df):
    for col in df.columns[3:]:
        col = str(col)
        year = int(col[6:10])
        prev_yr = year - 1
        df[col] = update_threat(df, prev_yr, year)


def process_loc_data():
    print('running process loc data')
    # clean up data to match other data
    filename = os.path.join('Table_7_Loc_Data', 'msw3-all.pdf')
    # loc = pd.DataFrame()
    # next_pages = pd.DataFrame()
    df_2 = pd.DataFrame()
    # curr_table = cm.read_pdf(filename, flavor='stream',
    #                          pages=str(1),
    #                          table_areas=['230, 3000, 1450, 200'])
    # df_1 = curr_table[0].df
    # print(df_1)
    # for i in range(2, 10):
    #     hold_df = pd.DataFrame()
    #     print('running 1 ' + str(i))
    #     curr_table = cm.read_pdf(filename, flavor='stream',
    #                              pages=str(i),
    #                              table_areas=['230, 3000, 1450, 200'])
    #     hold_df = curr_table[0].df
    #     next_pages = next_pages.append(hold_df, ignore_index=True)
    # print(next_pages)
    # df_1 = df_1.append(next_pages)
    for i in range(107, 108):
        hold_df = pd.DataFrame()
        print('running 2 ' + str(i))
        curr_table = cm.read_pdf(filename, flavor='stream',
                                 pages=str(i),
                                 table_areas=['810, 2900, 2000, 300'])
                                #  columns=['900, 940, 1360'])
        hold_df = curr_table[0].df
        df_2 = df_2.append(hold_df, ignore_index=True)
    print('done with loops')
    # drop the extra info on top, make row 1 the column names
    # next_pages['Scientific name'] = next_pages[5] + ' ' + next_pages[6]
    # next_pages = next_pages[[0, 'Scientific name']]
    # print(df_1)
    # # df_1.columns = df_1.iloc[0]
    # # drop column names from data
    # df_1 = df_1.drop([0])
    # df_1 = df_1[['ID', 'Genus', 'Species']]
    # print(df_1)
    # print(df_1.columns)
    # print(df_2)
    # make row 1 the column names
    df_2.columns = df_2.iloc[0]
    # drop column names from data
    df_2 = df_2.drop([0])
    df_2['Location'] = df_2['TypeLocality'].apply(first_loc)
    df_2 = df_2[['ID', 'CommonName', 'Location']]
    # print(df_2['CommonName'])
    # print('df 1')
    # print(df_1)
    # loc = pd.merge(df_1, df_2,
    #                on=['ID'], how='outer')
    # loc['Scientific name'] = loc['Genus'] + ' ' + loc['Species']
    # loc = loc[['Scientific name', 'CommonName', 'Location']]
    # print(loc.columns)
    # loc = loc.rename(columns={'CommonName': 'Common name'})
    # next_pages.to_csv('checking_1.2.csv')
    # df_1.to_csv('checking_part_1.csv')
    df_2.to_csv('checking part_2.csv')
    # loc.to_csv('mammal_location_2.csv')
    # print(loc)

def process_big_data() -> pd.DataFrame:
    """
    Not complete docstring
    lots of if statements because the files are all read differently by
    camelot
    """
    print('running process big data')
    merged_df = pd.DataFrame(columns=['Scientific name'])
    # go through each file in the folder
    for pdf_name in os.listdir('Table_7_Loc_Data'):
        filename = os.path.join('Table_7_Loc_Data', pdf_name)
        # if the file is the right pdf
        if (pdf_name[-4:] == '.pdf') and (pdf_name != 'msw3-all.pdf') and (pdf_name != 'msw3-all-2.pdf'):
            yr = int(pdf_name[0:4])
            print(yr)
            fin_df = pd.DataFrame()
            for i in range(1, 40):
                # read and create a dataframe for each pdf
                hold_df = pd.DataFrame()
                try:
                    if yr == 2008 and i == 1:
                        curr_table = cm.read_pdf(filename,
                                                 flavor='stream',
                                                 pages=str(i),
                                                 table_areas=['0,790,1000,0'])
                        hold_df = curr_table[0].df
                    elif yr == 2009 and i == 1:
                        curr_table = cm.read_pdf(filename,
                                                 flavor='stream',
                                                 pages=str(i),
                                                 table_areas=['0,910,1000,0'])
                        hold_df = curr_table[0].df
                    else:
                        curr_table = cm.read_pdf(filename,
                                                 flavor='stream',
                                                 pages=str(i))
                        hold_df = curr_table[0].df
                    fin_df = fin_df.append(hold_df, ignore_index=True)
                except IndexError:
                    break
            # each individual pdf is processed differently by camelot
            if yr >= 2011 and yr <= 2013:
                fin_df.columns = fin_df.iloc[12]
                fin_df = fin_df.drop(fin_df.index[0:15])
            elif yr == 2008 or yr == 2009 or yr == 2007:
                fin_df.columns = fin_df.iloc[2]
                fin_df = fin_df.drop(fin_df.index[0:5])
            elif yr == 2010:
                fin_df.columns = fin_df.iloc[16]
                fin_df = fin_df.drop(fin_df.index[0:19])
            elif yr >= 2014 and yr <= 2021:
                fin_df.columns = fin_df.iloc[13]
                fin_df = fin_df.drop(fin_df.index[0:16])
            fin_df = fin_df.drop(columns=['(' + str(yr - 1) + ')'])
            # reset indexing (important for math later on)
            new_indexing = list(range(len(fin_df)))
            fin_df['index'] = new_indexing
            fin_df = fin_df.set_index('index', drop=True)
            # find the index of each class of animal
            if yr < 2020:
                classes = CLASSES_1
            else:
                classes = CLASSES_2
            index_list = []
            for cls in classes:
                if cls == 'MAMMALS' and yr == 2008:
                    index_list.append(('mammals', 0))
                else:
                    try:
                        if yr >= 2020:
                            space = (cls.index('(')) - 1
                            cl = cls[:space].lower()
                        else:
                            cl = cls.lower()
                        i = fin_df.index[fin_df['Scientific name'] == cls
                                         ].tolist()
                        if i != []:
                            index_list.append((cl, i[0]))
                    except IndexError:
                        continue
            index_list = sorted(index_list, key=itemgetter(1))
            # for each of these classes, add the number of rows as there are
            # number of animals in that class. this creates a list that we
            # can add to the resulting df as a new column
            new_col = []
            for n in range(0, (len(index_list))):
                curr_index = index_list[n][1]
                if n == (len(index_list) - 1):
                    next_index = len(fin_df)
                else:
                    next_index = index_list[n + 1][1]
                num = next_index - curr_index
                hold = []
                hold = [index_list[n][0]] * num
                new_col.extend(hold)
            if yr != 2009:
                fin_df = fin_df.rename(columns={'': 'Reason for change'})
                # keeping everything that has no common name but is an animal
            elif yr == 2009:
                fin_df = fin_df.rename(columns={'for': 'Reason for change',
                                                'List (2009.2)':
                                                'List (2009)'})
            fin_df['Common name'] = fin_df['Common name'].replace('', 'NaN')
            # don't keep anything that doesn't have a scientific name
            fin_df['Scientific name'] = fin_df['Scientific name'
                                               ].replace('Scientific name',
                                                         np.nan)
            fin_df['Scientific name'] = fin_df['Scientific name'
                                               ].replace('', np.nan)
            if yr == 2008:
                # don't keep anythign that is a header
                fin_df['List (2008)'] = fin_df['List (2008)'
                                               ].replace('', np.nan)
            if yr != 2008:
                # don't keep anything that is a non-genuine change
                # 2008 doesn't have this column name
                fin_df['Reason for change'] = fin_df['Reason for change'
                                                     ].replace('N', np.nan)
                # fin_df['Reason for change'] = fin_df['Reason for change'
                #                                      ].replace('E', np.nan)
                fin_df['Reason for change'] = fin_df['Reason for change'
                                                     ].replace('', np.nan)
            # don't keep anythign that is data deficient
            fin_df['List (' + str(yr) + ')'] = fin_df['List (' + str(yr) + ')'
                                                      ].replace('DD', np.nan)
            fin_df['Class'] = new_col
            fin_df = fin_df.dropna()
            if yr != 2008:
                fin_df = fin_df.drop(columns=['Reason for change'])
            merged_df = pd.merge(merged_df, fin_df, how='outer')
    merged_df = merged_df.apply(fill_in_threat())
    merged_df = merged_df[['Scientific name', 'Common name', 'Class',
                           'List (2007)', 'List (2008)', 'List (2009)',
                           'List (2010)', 'List (2011)', 'List (2012)',
                           'List (2013)', 'List (2014)', 'List (2015)',
                           'List (2016)', 'List (2017)', 'List (2018)',
                           'List (2019)', 'List (2020)', 'List (2021)']]
    merged_df = fill_in_threat(merged_df)
    loc_data = pd.read_csv('location.csv')
    merged_df = pd.merge(merged_df, loc_data, left_on='Scientific name',
                         right_on='Scientific name', how='outer')
    # to save to csv for testing purposes
    merged_df.to_csv('final_combined_data')
    return(merged_df)


<<<<<<< HEAD
data = process_loc_data()
# data = process_big_data()
# data = pd.read_csv('checking part_2.csv')
# print(data)
# print(data['8'])
# data = pd.read_csv('testing_red_list_processing.cvs')
# print(data.columns)


# modifying the data in each year to match the previous year
# test_set = pd.read_csv('testing_red_list_processing.cvs')
# test_set = test_set.astype(str)
# test_set = test_set[['Scientific name', 'Common name', 'Class',
#                      'List (2007)', 'List (2008)', 'List (2009)',
#                      'List (2010)', 'List (2011)', 'List (2012)',
#                      'List (2013)', 'List (2014)', 'List (2015)',
#                      'List (2016)', 'List (2017)', 'List (2018)',
#                      'List (2019)', 'List (2020)', 'List (2021)']]
# fill_in_threat()


# print(test_set)
# print(test_set['List (2017)'])
# year = 2017
# # prev_yr = 'List (2016)'
# prev_yr = 2016
# print(test_set['List (2017)'])
# test_set['List (2017)'] = test_set['List (2017)'].apply(update_threat(prev_yr, year))
# test_set['List (2017)'] = test_set['List (2017)'].where(test_set['List (2017)'] != 'nan', test_set['List (2016)'])
# print(test_set['List (2017)'])


# test_set['List (2017)'] = test_set['List (2017)'].replace('nan', test_set['List (2016)'], inplace=True)
# print(test_set['List (2016)'])
=======
# process_loc_data(DIRECTORY)
data = process_big_data()
print(data)
>>>>>>> 62aa67d5a8838048d2ef68018b3064100d02be0d
