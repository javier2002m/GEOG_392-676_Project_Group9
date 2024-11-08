# import os
import pandas as pd
import geopandas as gpd
# import matplotlib

""" Folder path for datasets """
data_folder_path = r'/Users/javiermendez/Documents/Classes/Fall2024/GEOG 392/Project Data'
data_output_folder = data_folder_path+r'/Data_Output'
""" NHD Texas State geopackage """
NHD_path = data_folder_path+r'/NHD_H_Texas_State_GPKG'
NHD_gpkg = NHD_path+r'/NHD_H_Texas_State_GPKG.gpkg'
""" NRI Table Census Tracts in Texas """
NRI_path = data_folder_path+r'/NRI_Table_CensusTracts_Texas'
NRI_csv = NRI_path+r'/NRI_Table_CensusTracts_Texas.csv'
NRI_dict = NRI_path+r'/NRIDataDictionary.csv'
""" load data into GeoDataFrame """
nri_csv_readfile = gpd.read_file(NRI_csv)
nri_dict_readfile = gpd.read_file(NRI_dict)