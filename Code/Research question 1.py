import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from utils import extinction_level_numerical, avg_tl_change_multiple_years

"""
List of variables/strings that need to be changed when data processing complete:

2007-2021 csv filename --> filepath for processed extinction data
Change all year ranges to cover all data
"""




def main():
    # Will probably not have to dropna once data is processed
    df = pd.read_csv("Book1.csv")
    df = df.dropna()
    # Create dataframe with numerical values for extinction threat level in given year range
        # Create new dataframe including species name, class, average threat level
    mini_df = df[["Common name", "Class", "List (2007)", "List (2008)", "List (2009)"]]
    # mini_df = df[["Common name", "Class", "List (2007)", "List (2008)",
    #               "List (2009)", "List (2010)", "List (2011)",
    #               "List (2012)", "List (2013)", "List (2013)",
    #               "List (2014)", "List (2015)", "List (2016)",
    #               "List (2017)", "List (2018)", "List (2019)",
    #               "List (2020)", "List (2021)"]]
    for year in range(2007, 2010):
        numerical_exinction_category = extinction_level_numerical(str(year), mini_df)
        column_label = "List (" + str(year) + ")"
        # Replace string extinction threat level with the numerical value
        mini_df.loc[:, column_label] = numerical_exinction_category


    # Find average threat level change by year for each species
    
    species_threat_level_data = avg_tl_change_multiple_years(2007, 2009, mini_df)
        
    # Ask Rhea if I can take this out
    species_threat_level_change_df = mini_df[["Common name", "Class", "Average Species Threat Level Change 2007-2008",
                                              "Average Species Threat Level Change 2008-2009"]]

    # species_threat_level_change_df = mini_df[["Common name", "Class", "Average Species Threat Level Change 2007-2008",
    #                                           "Average Species Threat Level Change 2008-2009", "Average Species Threat Level Change 2009-2010",
    #                                           "Average Species Threat Level Change 2010-2011", "Average Species Threat Level Change 2011-2012",
    #                                           "Average Species Threat Level Change 2012-2013", "Average Species Threat Level Change 2013-2014",
    #                                           "Average Species Threat Level Change 2014-2015", "Average Species Threat Level Change 2015-2016",
    #                                           "Average Species Threat Level Change 2016-2017", "Average Species Threat Level Change 2017-2018",
    #                                           "Average Species Threat Level Change 2018-2019", "Average Species Threat Level Change 2019-2020",
    #                                           "Average Species Threat Level Change 2020-2021"]]

    
    # Use groupby to find the average threat level by class
    class_threat_level_by_year_df = pd.DataFrame()
    for year in range(2007, 2010):       
        class_threat_level = mini_df.groupby("Class")["List (" + str(year) + ")"].mean()
        class_threat_level_by_year_df[str(year)] = class_threat_level


    # Create line plot of change in average threat levels for each class between 2007 and 2021

    sns.relplot(data=class_threat_level_by_year_df.T, kind="line")
    plt.title("Class Exctinction Threat Levels 2007-2021")
    plt.xlabel("Year")
    plt.ylabel("Threat Level")
    plt.ylim(0, 7)
    plt.savefig("Threat Levels by Class 2007-2021.png", bbox_inches="tight")


if __name__ == "__main__":
   main()
   
   
