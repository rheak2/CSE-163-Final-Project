import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import csv_processing, species_threat_level_data_processing, \
                  process_big_data

"""
Giulia Clini, Elizabeth Karas, and Rhea Kulkarni
CSE 163 Final Project
This file contains the code required to answer research question 1. Firstly
it reads the data, and then it finds the top 5 species for average yearly
threat level change 2007-2021. Finally, it finds the average threat level
by class and returns a line graph visualising it.
"""

sns.set()


def do_question_1():
    '''
    This function will compute all of the calculations for the first research
    question, like calculating the top 5 vulnerable species and the plot of
    the average change in threat level for each class.
    '''
    df = process_big_data()
    mini_df = csv_processing(df)
    tl_data = species_threat_level_data_processing(mini_df)

    # Find species with top 5 average threat level change 2007-2021

    top_5 = tl_data[["Common name", "Average Yearly TL Change Over Time"]]
    top_5 = top_5.nlargest(5, "Average Yearly TL Change Over Time")
    # Uncomment line below to see top 5
    # print(top_5)

    # Use groupby to find the average threat level by class
    class_threat_level_by_year_df = pd.DataFrame()
    for year in range(2007, 2021):
        class_tl = mini_df.groupby("Class")["List (" + str(year) + ")"].mean()
        class_threat_level_by_year_df[str(year)] = class_tl

    # Create line plot of change in average threat levels for each class
    # between 2007 and 2021

    sns.relplot(data=class_threat_level_by_year_df.T, kind="line")
    plt.title("Class Exctinction Threat Levels 2007-2021")
    plt.xlabel("Year")
    plt.ylabel("Threat Level")
    plt.xticks(rotation=-45)
    plt.ylim(0, 8)
    plt.savefig("Threat Levels by Class 2007-2021.png", bbox_inches="tight")
