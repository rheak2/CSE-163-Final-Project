import pandas as pd
"""
Research question 1
"""
def main():
    df = pd.read_csv("Book1.csv")
    df = df.dropna()
    #mini_df = df[["Common name", "Class", "Kingdom", "IUCN Red List (2007) Category", "IUCN Red List (2021) Category"]]
    mini_df = df[["Common name", "IUCN Red List (2007) Category", "IUCN Red List (2021) Category"]]
    # Change extinction category from string to numeric value
    # Create dictionary mapping each extinction category to its numeric value
    extinction_category_dict = {"LC": 0, "NT": 1, "LR/cd": 2, "VU": 3, "EN": 4, "CR": 5, "EW": 6, "EX": 7, "DD": 1000}
    # Use the dictionary to convert to numeric value
    category_in_2007 = mini_df["IUCN Red List (2007) Category"]
    numerical_list = []
    for species in category_in_2007:
        numerical_list.append(extinction_category_dict[species])
    mini_df["IUCN Red List (2007) Category"] = numerical_list

    category_in_2021 = mini_df["IUCN Red List (2021) Category"]
    numerical_list = []
    for species in category_in_2021:
        numerical_list.append(extinction_category_dict[species])
    mini_df["IUCN Red List (2021) Category"] = numerical_list
    print(mini_df)

    # for species in mini_df:
    #     mini_df.loc[:, "Average Threat Level Change 2007-2021"] = (mini_df.loc[:, "IUCN Red List (2021) Category"] 
    #                                                              - mini_df.loc[:, "IUCN Red List (2007) Category"]) / 14

    kingdom_threat_level_change_between_years = pd.DataFrame()
    for year in range(2007, 2010):
        kingdom_threat_level_change = species_threat_level_change_df.groupby("Kingdom")["Average Species Threat Level Change " + str(year) + "-" + str(year + 1)].mean()
        kingdom_threat_level_change_between_years["Average Kingdom Threat Level Change " + str(year) + "-" + str(year + 1)] = kingdom_threat_level_change

        print(kingdom_threat_level_change_between_years)



def kingdom_threat_level_change_between_years(lower_year: int, upper_year: int, df: pd.DataFrame):
    """
    This method takes as argument any two consecutive years and a dataframe and adds a column
    to that dataframe showing the change in extinction threat level between those two years for
    all the kingdoms in the dataframe, using the groupby function.
    """
    year_range_string = str(lower_year) + "-" + str(upper_year)
    kingdom_extinction_threat_change = df.groupby("Kingdom")["Average Species Threat Level Change " + year_range_string].sum()
    return list(kingdom_extinction_threat_change)
       
def main():
    # Will probably not have to dropna once data is processed
    df = pd.read_csv("Book1.csv")
    df = df.dropna()
    # Create dataframe with numerical values for extinction threat level
        # Create new dataframe including species name, kingdom, average threat level
    mini_df = df[["Common name", "Kingdom", "IUCN Red List (2007) Category", "IUCN Red List (2021) Category"]]

    numerical_extinction_category_2007 = extinction_level_numerical("2007", mini_df)
    numerical_extinction_category_2021 = extinction_level_numerical("2021", mini_df)
        # Add column with numerical values of threat level to df
    mini_df["IUCN Red List (2007) Category"] = numerical_extinction_category_2007
    mini_df["IUCN Red List (2021) Category"] = numerical_extinction_category_2021
    print(mini_df)

if __name__ == "__main__":
    main()

"""
Research question 2
"""

