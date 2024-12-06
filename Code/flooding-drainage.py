import arcpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DB_PATH = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data"

arcpy.env.workspace = INPUT_DB_PATH

#paths to data
floodplain_data = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\100yrfloodplain_harris\houston-texas-100-year-flood-plain-harris-county.shp"
inadequate_drainage_data = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\HoustonDrainageSystems\InadequateDrainage_ExportFeatures.shp"
proposed_drainage_data = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\HoustonDrainageSystems\ProposedDrainage_ExportFeatures.shp"

#Ensure shapefiles use the same Coordinate System
target_ref = arcpy.Describe(floodplain_data).spatialReference

shapefiles = [
    r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\HoustonDrainageSystems\InadequateDrainage_ExportFeatures.shp",
    r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\HoustonDrainageSystems\ProposedDrainage_ExportFeatures.shp"
]

for shapefile in shapefiles:
    if arcpy.Describe(shapefile).spatialReference is None:
        arcpy.management.DefineProjection(shapefile, target_ref)


#Perform Count Overlapping Features
in_fcs = [floodplain_data, inadequate_drainage_data]
output_overlap1 = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\HoustonDrainageSystems\flooding-adequate_drainage_overlap.shp"
if not arcpy.Exists(output_overlap1):
    arcpy.analysis.CountOverlappingFeatures(in_fcs, output_overlap1, 2)
else:
    print(f"File already exists: {output_overlap1}")


in_fcs2 = [floodplain_data, proposed_drainage_data]
output_overlap2 = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\HoustonDrainageSystems\flooding-proposed_drainage_overlap.shp"
if not arcpy.Exists(output_overlap2):
    arcpy.analysis.CountOverlappingFeatures(in_fcs2, output_overlap2, 2)
else:
    print(f"File already exists: {output_overlap2}")