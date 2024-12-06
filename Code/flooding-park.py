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

if not arcpy.Exists(park_projection):
    # File does not exist, proceed with projection
    arcpy.management.Project(parksdata, park_projection, target_ref)
    print("Projection completed successfully!")
else:
    # File exists, handle this case
    print(f"Output file '{park_projection}' already exists. No action taken.")

#Perform Count Overlapping Features
in_fcs = [floodplain_data, parksdata]
output_overlap = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\Houston_Park_Greenspace\flooding-parks_overlap.shp"
if not arcpy.Exists(output_overlap):
    arcpy.analysis.CountOverlappingFeatures(in_fcs, output_overlap, 2)
else:
    print(f"File already exists: {output_overlap}")