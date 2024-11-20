import arcpy
import os

arcpy.env.workspace = r"rC:\Users\rober\GEOG 392\harriscounty_imperviousarea"

# Set the input and output paths
input_shapefile = r"C:\Users\rober\GEOG 392\harriscounty_imperviousarea"
output_shapefile = r"C:\Users\rober\GEOG_392-676_Project_Group9\Data\Harris_Impervious_Area"

# Dissolve the polygons based on a field (e.g., GRIDCODE)
arcpy.management.Dissolve(input_shapefile, output_shapefile)

