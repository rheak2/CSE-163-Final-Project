'''
Giulia Clini, Elizabeth Karas, and Rhea Kulkarni
CSE 163 Final Project
This file tests whether the data was correctly manipulated to implement
the third research question, which determines how reliable a decision
tree regression model is for predicting the average change in threat
level for a given species over 14 years.
'''

import rq3
import pandas as pd
import test_utils


def csv_to_df() -> pd.DataFrame:
    df = pd.read_csv('Code/Book1.csv')
    print(df)
    mini_df = test_utils.csv_processing(df)
    species_tl_data = test_utils.species_threat_level_data_processing(mini_df)
    return species_tl_data


def test_manipulate_data() -> None:
    '''
    This function tests that the manipulate_data
    function (from the output produced in csv_to_df).
    '''
    species_tl_df = csv_to_df()
    expected_num_cols = 9
    actual_num_cols = len(species_tl_df.columns)
    test_utils.assert_equals(expected_num_cols, actual_num_cols)



def main():
    test_manipulate_data()


if __name__ == '__main__':
    main()
