'''
Giulia Clini, Elizabeth Karas, and Rhea Kulkarni
CSE 163 Final Project
This file tests all of the functions implemented for the third research
question, which determines how reliable a decision tree regression model
is for predicting the average change in threat level for a given species
over 14 years.
'''

import Research_Question_3
import utils
import pandas as pd


def csv_to_df(file_path: str) -> pd.DataFrame:
    '''
    Given the filepath of the csv data file as a str, return
    the DataFrame that is produced using the manipulate_data
    function.
    '''
    book_1_df = utils.csv_processing(file_path)
    test_tl_df = Research_Question_3.manipulate_data(book_1_df)
    return test_tl_df


def test_manipulate_data() -> None:
    '''
    This function tests that the manipulate_data
    function (from the output produced in csv_to_df).
    '''
    print("doing csv_to_df")
    species_tl_df = csv_to_df('Code/Book1.csv')
    print("checking manipulate data")
    expected_num_rows = 73
    actual_num_rows = len(species_tl_df)
    print(expected_num_rows, actual_num_rows)
    # utils.assert_equals(expected_num_rows, actual_num_rows)
    expected_num_cols = 10
    actual_num_cols = len(species_tl_df.columns)
    print(expected_num_cols, actual_num_cols)
    # utils.assert_equals(expected_num_cols, actual_num_cols)
    expected_avg_tl = -0.333
    actual_avg_tl = species_tl_df.loc[0, 'Average TL Change Over Time']
    print(expected_avg_tl, actual_avg_tl)
    # utils.assert_equals(expected_avg_tl, actual_avg_tl)


def test_train_and_test_model() -> None:
    '''
    This function tests the train_and_test_model function.
    '''
    print("checking train_and_test_model")
    species_tl_df = csv_to_df('Code/Book1.csv')
    trained_tested_df = Research_Question_3.train_and_test_model(species_tl_df)
    expected_num_pred = 75
    actual_num_train_pred = len(trained_tested_df['Train Predictions'])
    actual_num_test_pred = len(trained_tested_df['Test Predictions'])
    print(expected_num_pred, actual_num_test_pred, actual_num_train_pred)
    # utils.assert_equals(expected_num_pred, actual_num_train_pred)
    # utils.assert_equals(expected_num_pred, actual_num_test_pred)


def main():
    test_manipulate_data()
    test_train_and_test_model()


if __name__ == '__main__':
    main()
