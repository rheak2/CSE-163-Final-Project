'''
docstring
'''

import pandas as pd


def process_data(file_name: str) -> pd.DataFrame:
    conservation_df: pd.DataFrame = pd.DataFrame(columns=('Country', 'Letter Index', 'Num Index'))
    letter_num_index: dict[str, int] = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
    with open(file_name) as f:
        lines: list[str] = f.readlines()
        for line_index in range(len(lines)):
            words: list[str] = lines[line_index].split(',')
            letter_index: str = words[1].strip()
            num_index: int = letter_num_index[letter_index]
            conservation_df = conservation_df.append({'Country': words[0], 'Letter Index': letter_index, 'Num Index' : num_index}, ignore_index=True)
    return conservation_df


def main():
    df = process_data('/Users/Rhea Kulkarni/CSE 163 Final Exam/Conservation Data/Conservation Data.txt')

if __name__ == '__main__':
    main()