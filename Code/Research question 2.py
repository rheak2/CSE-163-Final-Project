import pandas as pd
from utils import process_conservation_data, csv_processing, species_threat_level_data_processing, process_big_data
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import seaborn as sns
sns.set()

"""
Code to answer research question 2
How have conservation efforts affected the extinction and endangerment of mammals? 
"""

def conservation_rating_map(conservation_data, gdf):
    # Create a colour map showing the conservation ratings around the world for
    # the countries we have this data for
    
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


def threat_level_map(threat_data, gdf):
    # Create a colour coded map showing the average extinction threat level change
    # 2007-2021 around the world
 

    # ADD LOCATION TO THIS DF ONCE FULL DATASET AVAILABLE
    threat_data = threat_data[["Common name", "Average TL Change Over Time"]]
    print(threat_data)
    location_threat_geometry = threat_data.merge(gdf, left_on="Location", right_on="name", how="inner")
    print(location_threat_geometry)
    location_threat_geometry = gpd.GeoDataFrame(location_threat_geometry, geometry="geometry")
    # Plot a map of the average extinction threat level change around the world
    fig, ax = plt.subplots(nrows=1, figsize=(15, 7))
    gdf.plot(color="#EEEEEE", ax=ax)
    location_threat_geometry.plot(column="Average TL Change Over Time", ax=ax, legend=True)
    plt.title("Map of Extinction Threat Level Change 2007-2021")
    plt.savefig("Threat level change map.png")  


def scatter_plot(threat_data):
    # Create Scatter Plot


    # sns.set_style("ticks")

    scatter_plot_df = pd.DataFrame()
    scatter_plot_df["Average Yearly Threat Level Change 2007-2021"] = threat_data["Average TL Change Over Time"]
    scatter_plot_df["Conservation Efforts 2021"] = conservation_data["Num Index"]
    scatter_plot_df = scatter_plot_df.dropna()
    sns.relplot(data=scatter_plot_df, x="Conservation Efforts 2021", y="Average Yearly Threat Level Change 2007-2021")
    plt.xlabel("Conservation Efforts 2021")
    plt.ylabel("Average Yearly Threat Level Change 2007-2021")
    plt.title("Conservation Efforts vs Threat Level for Species in 2021")
    plt.savefig("Conservation vs threat level change scatterplot.png")

if __name__ == "__main__":
    conservation_data = process_conservation_data("Code/Conservation Data.txt")
    gdf = gpd.read_file("Code/countries.geo.json")
    df = process_big_data()
    extinction_data = csv_processing(df)
    print(extinction_data)
    conservation_rating_map(conservation_data)
    # threat_data = species_threat_level_data_processing(extinction_data)
    # print(threat_data)
    # conservation_rating_map(conservation_data, gdf)
    # # threat_level_map(threat_data, gdf)
    # scatter_plot(threat_data)

