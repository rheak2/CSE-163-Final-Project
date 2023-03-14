'''
Giulia Clini, Elizabeth Karas, and Rhea Kulkarni
CSE 163 Final Project
This file tests all of the functions implemented for the third research
question, which determines how reliable a decision tree regression model
is for predicting the average change in threat level for a given species
over 14 years.
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
    expected_num_cols = 8
    actual_num_cols = len(species_tl_df.columns)
    test_utils.assert_equals(expected_num_cols, actual_num_cols)


def test_train_and_test_model() -> None:
    '''
    This function tests the train_and_test_model function.
    '''
    print("checking train_and_test_model")
    species_tl_df = csv_to_df()
    trained_tested_df = rq3.train_and_test_model(species_tl_df)
    expected_num_pred = 75
    actual_num_train_pred = len(trained_tested_df['Train Predictions'])
    actual_num_test_pred = len(trained_tested_df['Test Predictions'])
    print(expected_num_pred, actual_num_test_pred, actual_num_train_pred)
    test_utils.assert_equals(expected_num_pred, actual_num_train_pred)
    test_utils.assert_equals(expected_num_pred, actual_num_test_pred)


def main():
    test_manipulate_data()
    test_train_and_test_model()


if __name__ == '__main__':
    main()
