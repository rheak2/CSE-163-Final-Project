import pandas as pd
from utils import process_conservation_data
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import seaborn as sns
sns.set()

"""
Code to answer research question 2
How have conservation efforts affected the extinction and endangerment of mammals? 
"""
# Create a colour map showing the conservation ratings around the world for
# the countries we have this data for
conservation_data = process_conservation_data("Conservation Data.txt")
gdf = gpd.read_file("countries.geo.json")
# Convert the integers of the conservation rating to floats so that map can be colour coded as gradient
conservation_data["Num Index"] = conservation_data["Num Index"].astype(float)
# Merge geometry data and conservation data, and then add geometry column to conservation
# data DataFrame
merged_data = conservation_data.merge(gdf, left_on="Country", right_on="name", how="inner")
merged_data = merged_data[["Country", "Num Index", "geometry"]]
merged_data = gpd.GeoDataFrame(merged_data, geometry="geometry")
# Plot a map of the conservation rating in all the countries
fig, ax = plt.subplots(nrows=1, figsize=(15, 7))
gdf.plot(color="#EEEEEE", ax=ax)
merged_data.plot(column="Num Index", ax=ax, legend=True, vmin=0)
plt.title("Map of Conservation Ratings for Countries with Data")
plt.savefig("Conservation map.png")

# Create a colour coded map showing the threat levels for animals around
# the world in 2021
