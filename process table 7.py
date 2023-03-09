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


def process_loc_data():
    print('running process loc data')
    # clean up data to match other data
    filename = os.path.join('Table 7. Loc Data', 'msw3-all.pdf')
    loc = pd.DataFrame()
    df_1 = pd.DataFrame()
    df_2 = pd.DataFrame()
    for i in range(1, 3):
        hold_df = pd.DataFrame()
        print('running 1' + str(i))
        curr_table = cm.read_pdf(filename, flavor='stream',
                                 pages=str(i),
                                 table_area=['0, 100, 100, 0'])
        print('done')
        hold_df = curr_table[0].df
        df_1 = df_1.append(hold_df, ignore_index=True)
    print(df_1)
    # for i in range(107, 109):
    #     hold_df = pd.DataFrame()
    #     print('running 2' + str(i))
    #     curr_table = cm.read_pdf(filename, flavor='stream',
    #                              pages=str(i),
    #                              columns=['358, 882, 965, 1389'])
    #     hold_df = curr_table[0].df
    #     df_2 = df_2.append(hold_df, ignore_index=True)
    # print('done with loops')
    # # drop the extra info on top, make row 1 the column names
    df_1.columns = df_1.iloc[0]
    # # drop column names from data
    df_1 = df_1.drop([0])
    # # make row 1 the column names
    # df_2.columns = df_2.iloc[0]
    # # drop column names from data
    # df_2 = df_2.drop([0])
    print(df_1.columns)
    # print(df_2.columns)
    print('df 1')
    print(df_1)
    # print(df_1['Genus'])
    # print(df_1['Extinct?'])
    # df_1 = df_1[['Genus', 'Species', 'ID']]
    # print('df 1')
    # print(df_1)
    # loc = pd.merge(df_1, df_2,
    #                on=['ID'], how='left')
    # loc['Scientific name'] = loc['Genus'] + ' ' + loc['Species']
    # loc = loc[['Scientific name', 'CommonName', 'TypeLocality']]
    # print()
    # print(loc['Scientific name'])
    # print()
    # print(loc['TypeLocality'])
    # loc = loc.rename(columns={'CommonName': 'Common name'})
    # print(loc['Common name'])
    # loc.to_csv('mammal_location_2.csv')


def process_big_data() -> pd.DataFrame:
    """
    Not complete docstring
    lots of if statements because the files are all read differently by
    camelot
    """
    print('running process big data')
    merged_df = pd.DataFrame(columns=['Scientific name'])
    # go through each file in the folder
    for pdf_name in os.listdir('Table 7. Loc Data'):
        filename = os.path.join('Table 7. Loc Data', pdf_name)
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
                fin_df['Reason for change'] = fin_df['Reason for change'
                                                     ].replace('E', np.nan)
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
    return(merged_df)
    # to save as CSV, uncomment code below, comment out return
    # if pdf_name != 'msw3-all.pdf':
    #     print(pdf_name)
    #     fin_df.to_csv(pdf_name + '.csv')


# process_loc_data(DIRECTORY)
data = process_big_data(DIRECTORY)
print(data)
