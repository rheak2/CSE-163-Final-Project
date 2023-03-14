import pandas as pd
import geopandas as gpd
import camelot as cm
import os
import numpy as np
from operator import itemgetter
import math
from typing import Any


def check_approx_equals(expected: Any, received: Any) -> bool:
    """
    Checks received against expected, and returns whether or
    not they match (True if they do, False otherwise).
    If the argument is a float, will do an approximate check.
    If the arugment is a data structure will do an approximate check
    on all of its contents.
    """
    try:
        if type(expected) == dict:
            # first check that keys match, then check that the
            # values approximately match
            return expected.keys() == received.keys() and \
                all([check_approx_equals(expected[k], received[k])
                    for k in expected.keys()])
        elif type(expected) == list or type(expected) == set:
            # Checks both lists/sets contain the same values
            return len(expected) == len(received) and \
                all([check_approx_equals(v1, v2)
                    for v1, v2 in zip(expected, received)])
        elif type(expected) == float:
            return math.isclose(expected, received, abs_tol=TOLERANCE)
        elif type(expected) == np.ndarray:
            return np.allclose(expected, received, atol=TOLERANCE,
                               equal_nan=True)
        elif type(expected) == pd.DataFrame:
            try:
                pd.testing.assert_frame_equal(expected, received,
                                              atol=TOLERANCE)
                return True
            except AssertionError:
                return False
        elif type(expected) == pd.Series:
            try:
                pd.testing.assert_series_equal(expected, received,
                                               atol=TOLERANCE)
                return True
            except AssertionError:
                return False
        else:
            return expected == received
    except Exception as e:
        print(f"EXCEPTION: Raised when checking check_approx_equals {e}")
        return False


def assert_equals(expected: Any, received: Any) -> None:
    """
    Checks received against expected, throws an AssertionError
    if they don't match. If the argument is a float, will do an approximate
    check. If the arugment is a data structure will do an approximate check
    on all of its contents.
    """

    if type(expected) == str:
        # Make sure strings have explicit quotes around them
        err_msg = f'Failed: Expected "{expected}", but received "{received}"'
    elif type(expected) in [np.ndarray, pd.Series, pd.DataFrame]:
        # Want to make multi-line output for data structures
        err_msg = f'Failed: Expected\n{expected}\n\nbut received\n{received}'
    else:
        err_msg = f'Failed: Expected {expected}, but received {received}'

    assert check_approx_equals(expected, received), err_msg


def csv_processing(df):
    # Will probably not have to dropna once data is processed
    # df = pd.read_csv(csv_filepath)
    # df = df.dropna()
    
    # Create dataframe with numerical values for extinction threat level in given year range
        # Create new dataframe including species name, class, average threat level
    mini_df = df[["Common name", "Class", "List (2007)", "List (2008)", "List (2009)"]]
    mini_df = mini_df.loc[mini_df['Class'].isin(["amphibians", "beetles", "birds"
                                                 "fishes", "crustaceans", "invertebrates",
                                                 "mammals", "reptiles"])]
    for year in range(2007, 2010):
        numerical_exinction_category = extinction_level_numerical(str(year), mini_df)
        column_label = "List (" + str(year) + ")"
        # Replace string extinction threat level with the numerical value
        mini_df.loc[:, column_label] = numerical_exinction_category
    
    return mini_df

def species_threat_level_data_processing(df):
    # Find average threat level change by year for each species
        
    species_threat_level_data = avg_tl_change_multiple_years(2007, 2009, df)
    return species_threat_level_data
    


def extinction_level_numerical(year: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    This methods  takes as argument the year, and returns a DataFrame
    showing the extinction threat level on a numerical scale from 0 to 8.
    NR stands for No Risk, and is used in cases where a species' first entry
    appears after 2007, in which case it is assumed that it previously faced
    no risk.
    """
    # Change extinction category from string to numeric value
    # Create dictionary mapping each extinction category to its numeric value
    extinction_category_dict = {"NR": 0, "LC": 1, "NT": 2, "LR/cd": 3, "VU": 4, "EN": 5, "CR": 6, "EW": 7, "EX": 8,\
                                    "CR (PE)": 6, "CR(PE)": 6, "CR(PEW)": 6}
    red_list_category = "List (" + year + ")"
    # Create list of all numerical values of extinction level in the year
    category_in_year = df[red_list_category]
    numerical_list = []
    for species in category_in_year:
        numerical_list.append(extinction_category_dict[species])
    return numerical_list


def tl_change_between_two_yrs(lower_year: int, upper_year: int, df: pd.DataFrame):
    """
    This method takes as argument any two consecutive years and a dataframe and adds a column
    to that dataframe showing the change in extinction threat level between those two years for
    all the species in the dataframe.
    """
    year_range_string = str(lower_year) + "-" + str(upper_year)
    lower_year_column = "List (" + str(lower_year) + ")"
    upper_year_column = "List (" + str(upper_year) + ")"
    df.loc[:, ["Species Threat Level Change " + year_range_string]] = \
          (df.loc[:, [upper_year_column]] - df.loc[:, [lower_year_column]])
    return df


def tl_change_between_multiple_yrs(lower_year: int, upper_year: int, df: pd.DataFrame):
    """
    This method takes as argument any range of years and a dataframe and adds columns
    to that dataframe showing the change in extinction threat level between consecutive years for
    all the species in the dataframe.
    """
    for year in range(lower_year, upper_year):
        df = tl_change_between_two_yrs(year, year + 1, df)
    return df


def avg_tl_change_multiple_years(lower_year: int, upper_year: int, data:pd.DataFrame) -> pd.DataFrame:
    """
    This method takes as argument any range of years and a dataframe and adds columns
    to that dataframe showing the average yearly change in extinction threat level over the
    year range for all species.
    """
    df = tl_change_between_multiple_yrs(lower_year, upper_year, data)
    year_range_length = upper_year - lower_year
    # Find mean of the threat level changes between all years and add this as a column
    # to the dataframe
    data['Average Yearly TL Change Over Time'] = df.iloc[:, year_range_length + 3:].mean(axis=1)
    return data


def process_conservation_data(file_path: str) -> pd.DataFrame:
    '''
    Given the path of the file as a string, returns a DataFrame
    storing each country in the World Animal Protection Index
    dataset, it's (letter) ranking, and a numerical index from
    1 to 7, with 1 corresponding to ranking 'A' and 7 to 'G'.
    '''
    
    # Create an empty DataFrame with the correct columns and a dictionary mapping
    # letter indices with numerical ones
    conservation_df: pd.DataFrame = pd.DataFrame(columns=('Country', 'Letter Index', 'Num Index'))
    letter_num_index: dict[str, int] = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}

    # Open the file and store each line in a list
    with open(file_path) as f:
        lines: list[str] = f.readlines()
        
        # For each line, split at the comma and store the country (first element in the
        # corresponding list), the letter index (the second element), and the numerical index
        # (from mapping in the letter_num_index dict) in three separate variables
        for line_index in range(len(lines)):
            words: list[str] = lines[line_index].split(',')
            letter_index: str = words[1].strip()
            num_index: int = letter_num_index[letter_index]
            
            # Append all three values as a row in the conservation_df DataFrame
            conservation_df = conservation_df.append({'Country': words[0], 'Letter Index': letter_index, 'Num Index' : num_index}, ignore_index=True)

    return conservation_df

def test_table_7_processing():
    test_2016 = pd.read_csv('2016.csv')
    assert_equals(103, len(test_2016))


def test_loc_processing():
    test_loc = pd.read_csv('mammal_location_data.csv')
    assert_equals(test_loc[test_loc['Common name']=='Short-beaked Echidna'].index.values[0],
                  test_loc[test_loc['Scientific name']=='Tachyglossus aculeatus'].index.values[0])
    assert_equals(test_loc[test_loc['Common name']=='Sir David’s Long-beaked Echidna.'].index.values[0],
                  test_loc[test_loc['Scientific name']=='Zaglossus attenboroughi'].index.values)
    assert_equals(test_loc[test_loc['Common name']=='Red-handed Howler'].index.values[0],
                  test_loc[test_loc['Scientific name']=='Alouattinae Alouatta'].index.values[1])


def test_final_df():
    test_df = pd.read_csv('final_combined_data')
    assert_equals(test_df[test_df['Scientific name']=='Dasyurus viverrinus'].index.values[0],
                  test_df[test_df['Location']=='Australia'].index.values[1])


test_table_7_processing()
test_loc_processing()
test_final_df()