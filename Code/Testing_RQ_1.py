import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from test_utils import csv_processing, species_threat_level_data_processing


"""
List of variables/strings that need to be changed when data processing complete:

2007-2021 csv filename --> filepath for processed extinction data
Change all year ranges to cover all data
"""


def main():
    df = pd.read_csv("Code/Book1.csv")
    df = df.dropna()
    mini_df = csv_processing(df)
    mini_df["Species THreat Level Change 2007-2008"] = (mini_df.loc[:, "List (2008)"] - mini_df.loc[:, "List (2007)"])
    print(mini_df)
    # species_threat_level_data = species_threat_level_data_processing(mini_df)
    
    

    # Find species with top 5 average threat level change 2007-2009

    top_5 = species_threat_level_data[["Common name", "Average Yearly TL Change Over Time"]]
    top_5 = top_5.nlargest(5, "Average Yearly TL Change Over Time")
    # print(top_5)
    

    # Use groupby to find the average threat level by class
    class_threat_level_by_year_df = pd.DataFrame()
    for year in range(2007, 2009):       
        class_threat_level = mini_df.groupby("Class")["List (" + str(year) + ")"].mean().reset_index()
        class_threat_level_by_year_df[str(year)] = class_threat_level


    # Create line plot of change in average threat levels for each class between 2007 and 2009

    # sns.relplot(data=class_threat_level_by_year_df.T, kind="line")
    # plt.title("Class Exctinction Threat Levels 2007-2009")
    # plt.xlabel("Year")
    # plt.ylabel("Threat Level")
    # plt.xticks(rotation=-45)
    # plt.ylim(0, 8)
    # plt.savefig("Threat Levels by Class 2007-2009.png", bbox_inches="tight")


if __name__ == "__main__":
   main()
