import pandas as pd
from utils import process_conservation_data
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

"""
Code to answer research question 2
How have conservation efforts affected the extinction and endangerment of mammals? 
"""



data = process_conservation_data("Conservation Data.txt")
print(data)


