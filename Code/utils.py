import pandas as pd
import geopandas as pgd


def extinction_level_numerical(year: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    This methods  takes as argument the year, and returns a DataFrame
    showing the extinction threat level on a numerical scale from 0 to 7.
    """
    # Change extinction category from string to numeric value
    # Create dictionary mapping each extinction category to its numeric value
    extinction_category_dict = {"LC": 0, "NT": 1, "LR/cd": 2, "VU": 3, "EN": 4, "CR": 5, "EW": 6, "EX": 7}
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
    df.loc[:, "Species Threat Level Change " + year_range_string] = \
          (df.loc[:, upper_year_column] - df.loc[:, lower_year_column])
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
    df = tl_change_between_multiple_yrs(lower_year, upper_year, data)
    year_range_length = upper_year - lower_year
    # Find mean of the threat level changes between all years and add this as a column
    # to the dataframe
    data['Average TL Change Over Time'] = df.iloc[:, year_range_length + 3:].mean(axis=1)
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
