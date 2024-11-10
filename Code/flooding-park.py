import arcpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DB_PATH = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data"


arcpy.env.workspace = INPUT_DB_PATH

#paths to data
floodplain_data = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\100yrfloodplain_harris\houston-texas-100-year-flood-plain-harris-county.shp"
parksdata = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\Houston_Park_GreenSpace\COH_HGAC_PARK_AREAS.shp"

#Ensure both shapefiles use the same Coordinate System
target_ref = arcpy.Describe(floodplain_data).spatialReference
park_projection = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\Houston_Park_Greenspace\Park_Areas_Projected.shp"
if arcpy.Describe(parksdata).spatialReference.factoryCode != target_ref.factoryCode:
    arcpy.Project_management(parksdata, park_projection, target_ref)
else:
    park_projection = parksdata

#Perform Count Overlapping Features
in_fcs = [floodplain_data, parksdata]
output_overlap = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\Houston_Park_Greenspace\flooding-parks_overlap.shp"
arcpy.analysis.CountOverlappingFeatures(in_fcs, output_overlap,2)