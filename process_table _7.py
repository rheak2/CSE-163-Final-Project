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


def update_threat(df, year_1, year_2):
    cy = 'List (' + str(year_2) + ')'
    py = 'List (' + str(year_1) + ')'
    if year_2 != 2007:
        df[cy] = df[cy].where(df[cy] != 'nan', df[py])
        return(df[cy])
    else:
        nt = ['NR'] * len(df[cy])
        df[cy] = df[cy].where(df[cy] != 'nan', nt)
        return(df[cy])


def fill_in_threat(df):
    for col in df.columns[3:]:
        col = str(col)
        year = int(col[6:10])
        prev_yr = year - 1
        df[col] = update_threat(df, prev_yr, year)
    return df


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
        if (pdf_name[-4:] == '.pdf') and (pdf_name != 'msw3-all.pdf'):
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
    # merged_df = merged_df.apply(fill_in_threat())
    merged_df = merged_df[['Scientific name', 'Common name', 'Class',
                           'List (2007)', 'List (2008)', 'List (2009)',
                           'List (2010)', 'List (2011)', 'List (2012)',
                           'List (2013)', 'List (2014)', 'List (2015)',
                           'List (2016)', 'List (2017)', 'List (2018)',
                           'List (2019)', 'List (2020)', 'List (2021)']]
    merged_df = merged_df.astype(str)
    merged_df = fill_in_threat(merged_df)
    loc_data = pd.read_csv('mammal_location_data.csv')
    loc_data = loc_data[['Scientific name', 'Common name', 'Location']]
    loc_data = loc_data.dropna(thresh=2)
    final_df = pd.merge(merged_df, loc_data, how='left')
    # to save for testing purposes, will remove before final submission
    final_df.to_csv('final_combined_data')
    return(final_df)


# EVERYTHING BELOW THIS LINE IS FOR TESTING PURPOSES
# AND RUNNING CERTAIN FUNCTIONS FOR TESTING
# df = pd.read_csv('final_combined_data')
# df = df.astype(str)
# df = df[['Scientific name', 'Common name', 'Class',
#                            'List (2007)', 'List (2008)', 'List (2009)',
#                            'List (2010)', 'List (2011)', 'List (2012)',
#                            'List (2013)', 'List (2014)', 'List (2015)',
#                            'List (2016)', 'List (2017)', 'List (2018)',
#                            'List (2019)', 'List (2020)', 'List (2021)']]
# print(df)
# df = fill_in_threat(df)
# # df = df.apply(fill_in_threat(df))
# print(df)
# print(update_and_merge(df))
# test_df = pd.read_csv()
# if '\n' in word:
#     word = word.split('\n')
#     test_df['Common name'] = word[0]
#     test_df['Location'] = word[1]
#     return (data['Common name', 'Location'])
# print(test_df['Common name'])
# def split(word):
#     if '\n' in word:
#         word = word.split('\n')
#         return (word[1])
# def repl(df, cn, loc):
#     # df[loc] = df[loc].where('\n' not in df[cn], df[cn][1].)
#     new_loc = df[cn].apply(split)
#     df[loc] = df[new_loc]
#     return (df[cn, loc])
# test_df = test_df.apply(repl(test_df, 'Common name', 'Location'))
# print(test_df)
