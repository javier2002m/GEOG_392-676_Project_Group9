import arcpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DB_PATH = r"C:Users\rober\GEOG_392-676_Project_Group9\Data"

arcpy.env.workspace = INPUT_DB_PATH

#paths to data
floodplain_data = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\100yrfloodplain_harris\houston-texas-100-year-flood-plain-harris-county.shp"
impervious_data = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\Impervious_Area\Harris_Impervious_Area.shp"

#Ensure shapefiles use the same Coordinate System
target_ref = arcpy.Describe(floodplain_data).spatialReference
impervious_projection = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\Impervious_Area\Impervious_Area_Projected.shp"

if not arcpy.Exists(impervious_projection):
    # File does not exist, proceed with projection
    arcpy.management.Project(impervious_data, impervious_projection, target_ref)
    print("Projection completed successfully!")
else:
    # File exists, handle this case
    print(f"Output file '{impervious_projection}' already exists. No action taken.")

#Count ovelapping feautes
in_fcs = [floodplain_data, impervious_data]
output_overlap = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\Impervious_Area\flooding-impervious.shp"
if not arcpy.Exists(output_overlap):
    arcpy.analysis.CountOverlappingFeatures(in_fcs, output_overlap, 2)
else:
    print(f"File already exists: {output_overlap}")