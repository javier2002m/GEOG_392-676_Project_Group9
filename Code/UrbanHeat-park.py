import arcpy
import os

# Allow overwriting of existing output files
arcpy.env.overwriteOutput = True

# Base Paths
INPUT_DB_PATH = r"C:\Users\rubia\OneDrive\Desktop\GIS PROGRAM PROJECT"
OUTPUT_DATA_PATH = os.path.join(INPUT_DB_PATH, "New_Data2")

# Set ArcPy workspace
arcpy.env.workspace = INPUT_DB_PATH

# Paths to Input Data
urban_heat_folder = r"C:\Users\rubia\OneDrive\Desktop\GIS PROGRAM PROJECT\UrbanHeatIslands_AM_AF_PM_HarrisCounty\UrbanHeatIslands_AM_AF_PM"
parks_data = r"C:\Users\rubia\OneDrive\Desktop\GIS PROGRAM PROJECT\Houston_Park_GreenSpace\COH_HGAC_PARK_AREAS\COH_HGAC_PARK_AREAS.shp"  # Update the extension if needed

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

    # Check if Urban Heat Island and Park shapefiles exist
    print(f"Processing {time_period} Urban Heat Island data for park intersect...")
    if arcpy.Exists(urban_heat_data) and arcpy.Exists(parks_data):
        # Re-project Park Areas if necessary to match the CRS of Urban Heat Island data
        urban_heat_ref = arcpy.Describe(urban_heat_data).spatialReference
        projected_parks = os.path.join(OUTPUT_DATA_PATH, f"Parks_Projected_{time_period}.shp")

        if arcpy.Describe(parks_data).spatialReference.factoryCode != urban_heat_ref.factoryCode:
            arcpy.management.Project(parks_data, projected_parks, urban_heat_ref)
            print(f"Park areas projected to match {time_period} Urban Heat CRS.")
        else:
            projected_parks = parks_data

        # Repair geometries before intersect analysis
        arcpy.management.RepairGeometry(urban_heat_data)
        arcpy.management.RepairGeometry(projected_parks)

        # Perform intersection analysis
        urban_heat_parks_output = os.path.join(OUTPUT_DATA_PATH, f"{time_period}_UrbanHeat_Parks_Intersect.shp")
        arcpy.analysis.Intersect([urban_heat_data, projected_parks], urban_heat_parks_output, "ALL")
        print(f"{time_period} Urban Heat and Parks intersection completed. Output saved to {urban_heat_parks_output}.")
    else:
        print(f"One or more input files are missing for {time_period}. Skipping.")