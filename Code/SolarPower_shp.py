import arcpy
import os

""" Data Folder Paths """
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DATA_PATH = r"\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-857847\Downloads\Project data"
SolarPower_Data = INPUT_DATA_PATH+r"\108Table_HoustonIrradianceAlbedo.csv"
OUTPUT_DATA_Path = INPUT_DATA_PATH+r"\New_Data"
# \\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-857847\Downloads\Project data\New_Data

""" Create GDB and setup workspace """
arcpy.management.CreateFileGDB(OUTPUT_DATA_Path, "SolarPower.gdb") # Create a new geodatabase for the Solar Power Dataset
Solar_Power_GDB = OUTPUT_DATA_Path+"\SolarPower.gdb" # Path to new gdb
arcpy.env.workspace = Solar_Power_GDB # Set Work Environment to new gdb

""" Create Point Layer from Solar Power dataset """
arcpy.management.XYTableToPoint(SolarPower_Data, 'Solar_Power_108', 'LON', 'LAT') # create solar power shapefile