'''
Giulia Clini, Elizabeth Karas, and Rhea Kulkarni
CSE 163 Final Project
This file tests all of the functions implemented for the first research question,
which determines which species in the dataset are most vulnerable to extinction.
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from utils import csv_processing, species_threat_level_data_processing


"""
List of variables/strings that need to be changed when data processing complete:

2007-2021 csv filename --> filepath for processed extinction data
Change all year ranges to cover all data
"""


def main():
    # Will probably not have to dropna once data is processed
    df = pd.read_csv("Book1.csv")
    df = df.dropna()
    
    mini_df = csv_processing("Code/Book1.csv")
    species_threat_level_data = species_threat_level_data_processing(mini_df)

    # Find species with top 5 average threat level change 2007-2021

    top_5 = species_threat_level_data[["Common name", "Average TL Change Over Time"]]
    top_5 = top_5.nlargest(5, "Average TL Change Over Time")
    print(top_5)
    

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
