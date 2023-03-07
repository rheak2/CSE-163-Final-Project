'''
Giulia Clini, Elizabeth Karas, and Rhea Kulkarni
CSE 163 Final Project
This file reads a hardcoded txt file storing the World Animal Protection index
for each country in the database and produces a pandas DataFrame with both
values plus a hardcoded numerical ranking for 1 to 7.
'''

import pandas as pd


def process_data(file_path: str) -> pd.DataFrame:
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
    with open(file_name) as f:
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


def main():
    df = process_data('/Users/Rhea Kulkarni/CSE 163 Final Exam/Conservation Data/Conservation Data.txt')

if __name__ == '__main__':
    main()
