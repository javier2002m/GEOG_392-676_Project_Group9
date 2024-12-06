import arcpy
import os

# Allow overwriting of existing output files
arcpy.env.overwriteOutput = True

# Base Paths
INPUT_DB_PATH = r"C:\Users\rubia\OneDrive\Desktop\GIS PROGRAM PROJECT"
OUTPUT_DATA_PATH = os.path.join(INPUT_DB_PATH, "New_Data3")

# Set ArcPy workspace
arcpy.env.workspace = INPUT_DB_PATH

# Paths to Input Data
impervious_data = r"C:\Users\rubia\OneDrive\Desktop\GIS PROGRAM PROJECT\Harris_Impervious_Area\Harris_Impervious_Area.shp"
inadequate_drainage_data = r"C:\Users\rubia\OneDrive\Desktop\GIS PROGRAM PROJECT\HoustonDrainageSystems\InadequateDrainage_ExportFeatures.shp"
proposed_drainage_data = r"C:\Users\rubia\OneDrive\Desktop\GIS PROGRAM PROJECT\HoustonDrainageSystems\ProposedDrainage_ExportFeatures.shp"

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DATA_PATH):
    os.makedirs(OUTPUT_DATA_PATH)

# List of Drainage System datasets and their corresponding names
drainage_datasets = {
    "Inadequate_Drainage": inadequate_drainage_data,
    "Proposed_Drainage": proposed_drainage_data
}

# Loop through each Drainage System dataset
for drainage_name, drainage_path in drainage_datasets.items():
    print(f"Processing Impervious Area and {drainage_name} intersect analysis...")

    if arcpy.Exists(impervious_data) and arcpy.Exists(drainage_path):
        # Ensure both datasets use the same Coordinate System
        impervious_ref = arcpy.Describe(impervious_data).spatialReference
        projected_drainage = os.path.join(OUTPUT_DATA_PATH, f"{drainage_name}_Projected.shp")

        if arcpy.Describe(drainage_path).spatialReference.factoryCode != impervious_ref.factoryCode:
            arcpy.management.Project(drainage_path, projected_drainage, impervious_ref)
            print(f"{drainage_name} re-projected to match Impervious Area CRS.")
        else:
            projected_drainage = drainage_path

        # Repair geometries before intersect analysis
        arcpy.management.RepairGeometry(impervious_data)
        arcpy.management.RepairGeometry(projected_drainage)

        # Perform intersection analysis
        impervious_drainage_output = os.path.join(OUTPUT_DATA_PATH, f"Impervious_Area_{drainage_name}_Intersect.shp")
        arcpy.analysis.Intersect([impervious_data, projected_drainage], impervious_drainage_output, "ALL")
        print(f"Impervious Area and {drainage_name} intersection completed. Output saved to {impervious_drainage_output}.")
    else:
        print(f"One or more input files are missing for {drainage_name}. Skipping.")