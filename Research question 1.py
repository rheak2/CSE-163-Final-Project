import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

"""
List of variables/strings that need to be changed when data processing complete:

2007-2021 csv filename --> filepath for processed extinction data
Change all year ranges to cover all data
"""

def extinction_level_numerical(year: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    This methods converts takes as argument the year, and for returns a DataFrame
    showing the extinction threat level on a numerical scale from 0 to 7.
    """
    # Change extinction category from string to numeric value
    # Create dictionary mapping each extinction category to its numeric value
    extinction_category_dict = {"LC": 0, "NT": 1, "LR/cd": 2, "VU": 3, "EN": 4, "CR": 5, "EW": 6, "EX": 7}
    red_list_category = "IUCN Red List (" + year + ") Category"
    # Create list of all numerical values of extinction level in the year
    category_in_year = df[red_list_category]
    numerical_list = []
    for species in category_in_year:
        numerical_list.append(extinction_category_dict[species])
    return numerical_list

def species_threat_level_change_between_years(lower_year: int, upper_year: int, df: pd.DataFrame):
    """
    This method takes as argument any two consecutive years and a dataframe and adds a column
    to that dataframe showing the change in extinction threat level between those two years for
    all the species in the dataframe.
    """
    year_range_string = str(lower_year) + "-" + str(upper_year)
    lower_year_column = "IUCN Red List (" + str(lower_year) + ") Category"
    upper_year_column = "IUCN Red List (" + str(upper_year) + ") Category"
    for species in df:
        df.loc[:, "Average Species Threat Level Change " + year_range_string] = (df.loc[:, upper_year_column] - 
                                                                         df.loc[:, lower_year_column])
    return df



def main():
    # Will probably not have to dropna once data is processed
    df = pd.read_csv("Book1.csv")
    df = df.dropna()
    # Create dataframe with numerical values for extinction threat level in given year range
        # Create new dataframe including species name, kingdom, average threat level
    mini_df = df[["Common name", "Kingdom", "IUCN Red List (2007) Category", "IUCN Red List (2008) Category", "IUCN Red List (2009) Category"]]
    # mini_df = df[["Common name", "Kingdom", "IUCN Red List (2007) Category", "IUCN Red List (2008) Category",
    #               "IUCN Red List (2009) Category", "IUCN Red List (2010) Category", "IUCN Red List (2011) Category",
    #               "IUCN Red List (2012) Category", "IUCN Red List (2013) Category", "IUCN Red List (2013) Category",
    #               "IUCN Red List (2014) Category", "IUCN Red List (2015) Category", "IUCN Red List (2016) Category",
    #               "IUCN Red List (2017) Category", "IUCN Red List (2018) Category", "IUCN Red List (2019) Category",
    #               "IUCN Red List (2020) Category", "IUCN Red List (2021) Category"]]
    for year in range(2007, 2010):
        numerical_exinction_category = extinction_level_numerical(str(year), mini_df)
        column_label = "IUCN Red List (" + str(year) + ") Category"
        # Replace string extinction threat level with the numerical value
        mini_df.loc[:, column_label] = numerical_exinction_category


    # Find average threat level change by year for each species
    
    for year in range(2007, 2009):
        species_threat_level_change_between_years(year, year + 1, mini_df)
        
    # Ask Rhea if I can take this out
    species_threat_level_change_df = mini_df[["Common name", "Kingdom", "Average Species Threat Level Change 2007-2008",
                                              "Average Species Threat Level Change 2008-2009"]]

    # species_threat_level_change_df = mini_df[["Common name", "Kingdom", "Average Species Threat Level Change 2007-2008",
    #                                           "Average Species Threat Level Change 2008-2009", "Average Species Threat Level Change 2009-2010",
    #                                           "Average Species Threat Level Change 2010-2011", "Average Species Threat Level Change 2011-2012",
    #                                           "Average Species Threat Level Change 2012-2013", "Average Species Threat Level Change 2013-2014",
    #                                           "Average Species Threat Level Change 2014-2015", "Average Species Threat Level Change 2015-2016",
    #                                           "Average Species Threat Level Change 2016-2017", "Average Species Threat Level Change 2017-2018",
    #                                           "Average Species Threat Level Change 2018-2019", "Average Species Threat Level Change 2019-2020",
    #                                           "Average Species Threat Level Change 2020-2021"]]

    
    # Use groupby to find the average threat level by kingdom
    kingdom_threat_level_by_year_df = pd.DataFrame()
    for year in range(2007, 2010):       
        kingdom_threat_level = mini_df.groupby("Kingdom")["IUCN Red List (" + str(year) + ") Category"].mean()
        kingdom_threat_level_by_year_df[str(year)] = kingdom_threat_level


    # Create line plot of change in average threat levels for each kingdom between 2007 and 2021

    sns.relplot(data=kingdom_threat_level_by_year_df.T, kind="line")
    plt.title("Kingdom Exctinction Threat Levels 2007-2021")
    plt.xlabel("Year")
    plt.ylabel("Threat Level")
    plt.ylim(0, 7)
    plt.savefig("Threat Levels by Kingdom 2007-2021.png", bbox_inches="tight")


if __name__ == "__main__":
   main()
   
   