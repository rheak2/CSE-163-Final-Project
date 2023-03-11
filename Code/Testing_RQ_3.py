'''
Giulia Clini, Elizabeth Karas, and Rhea Kulkarni
CSE 163 Final Project
This file tests all of the functions implemented for the third research question,
which determines how reliable a decision tree regression model is for predicting
the average change in threat level for a given species over 14 years.
'''

import Research_Question_3.py
import utils.py

def test_manipulate_data() -> None:
    book_1_df = utils.csv_processing('Code\Book1.csv')
    species_tl_df = utils.species_threat_level_data_processing(book_1_df)


def test_train_and_test_model() -> None:
    pass