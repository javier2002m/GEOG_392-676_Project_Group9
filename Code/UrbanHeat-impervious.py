import arcpy
import os

# Allow overwriting of existing output files
arcpy.env.overwriteOutput = True

# Base Paths
INPUT_DB_PATH = r"C:\Users\rubia\OneDrive\Desktop\GIS PROGRAM PROJECT"
OUTPUT_DATA_PATH = os.path.join(INPUT_DB_PATH, "New_Data")

# Set ArcPy workspace
arcpy.env.workspace = INPUT_DB_PATH

# Paths to Input Data
urban_heat_folder = r"C:\Users\rubia\OneDrive\Desktop\GIS PROGRAM PROJECT\UrbanHeatIslands_AM_AF_PM_HarrisCounty\UrbanHeatIslands_AM_AF_PM"
impervious_data = r"C:\Users\rubia\OneDrive\Desktop\GIS PROGRAM PROJECT\Harris_Impervious_Area\Harris_Impervious_Area.shp"

# Time periods for Urban Heat Island and their corresponding filenames
heat_island_times = {
    "Morning": "UHI_AM_Temperature",
    "Afternoon": "UHI_AF_Temperature",
    "Evening": "UHI_PM_Temperature"
}

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DATA_PATH):
    os.makedirs(OUTPUT_DATA_PATH)

# Loop through each time period
for time_period, file_name in heat_island_times.items():
    # Path to the Urban Heat Island shapefile for the specific time period
    urban_heat_data = os.path.join(urban_heat_folder, time_period, f"{file_name}.shp")

    # Check if Urban Heat Island and Impervious Area shapefiles exist
    print(f"Processing {time_period} Urban Heat Island data...")
    if arcpy.Exists(urban_heat_data) and arcpy.Exists(impervious_data):
        # Re-project Impervious Areas if necessary to match the CRS of Urban Heat Island data
        urban_heat_ref = arcpy.Describe(urban_heat_data).spatialReference
        projected_impervious = os.path.join(OUTPUT_DATA_PATH, f"Impervious_Area_Projected_{time_period}.shp")

        if arcpy.Describe(impervious_data).spatialReference.factoryCode != urban_heat_ref.factoryCode:
            arcpy.management.Project(impervious_data, projected_impervious, urban_heat_ref)
            print(f"Impervious Areas projected to match {time_period} Urban Heat CRS.")

        # Repair geometries before intersect analysis
        arcpy.management.RepairGeometry(urban_heat_data)
        arcpy.management.RepairGeometry(projected_impervious)

        # Perform intersection analysis
        urban_heat_impervious_output = os.path.join(OUTPUT_DATA_PATH, f"{time_period}_UrbanHeat_Impervious_Intersect.shp")
        arcpy.analysis.Intersect([urban_heat_data, projected_impervious], urban_heat_impervious_output, "ALL")
        print(f"{time_period} Urban Heat and Impervious Areas intersection completed. Output saved to {urban_heat_impervious_output}.")
    else:
        print(f"One or more input files are missing for {time_period}. Skipping.")

    
layer_path = r"C:\Users\rubia\OneDrive\Desktop\GIS PROGRAM PROJECT\New_Data\Morning_UrbanHeat_Impervious_Intersect.shp"
fields = arcpy.ListFields(layer_path)
