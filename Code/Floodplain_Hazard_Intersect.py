import arcpy
import os

""" Data Folder Paths """
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DATA_PATH = r"\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-857847\Downloads\Project data"
OUTPUT_DB_PATH = INPUT_DATA_PATH+r"\New_Data" # The spatial analysis layers will be saved to a new spatial analysis gdb/folder

""" Floodplain and NRI Hazard layer paths """
Floodplain_Data = INPUT_DATA_PATH+r"\100yrfloodplain_harris\100yrfloodplain_harris\houston-texas-100-year-flood-plain-harris-county.shp"
NRI_GDB = OUTPUT_DB_PATH+r"\NRI_CensusTracts_Hazards_shp.gdb"
NRI_Hazards = NRI_GDB+r"\NRI_Shapefile_CensusTracts_HarrisCO"
RiverineFlooding = NRI_GDB+r"\RiverineFlooding_shp_NRI_CensusTracts_HarrisCo"
CoastalFlooding = NRI_GDB+r"\CoastalFlooding_shp_NRI_CensusTracts_HarrisCo"
Hurricane = NRI_GDB+r"\Hurricane_shp_NRI_CensusTracts_HarrisCo"
""" List of hazard paths """
hazards_list = [RiverineFlooding, CoastalFlooding, Hurricane]
hazards_name = ["RiverineFlooding", "CoastalFlooding", "Hurricane"]

""" Create GDB and setup workspace """
# arcpy.management.CreateFileGDB(OUTPUT_DB_PATH, "Floodplain_Hazard_Overlap.gdb") # Create a new geodatabase for the Overlapping Dataset
Floodplain_Hazard_gdb = OUTPUT_DB_PATH+"\Floodplain_Hazard_Intersect.gdb" # Path to new gdb
arcpy.env.workspace = Floodplain_Hazard_gdb # Set Work Environment to new path/gdb

""" Ensure both shapefiles use the same Coordinate System """
floodplain_ref = arcpy.Describe(Floodplain_Data).spatialReference
for hazard in range(len(hazards_list)):
    hazard_path = hazards_list[hazard] # path to iterated hazard list item
    new_hazard_file = hazards_name[hazard] # name of iterated hazard list
    projected_hazard = hazard_path
    """ Determine coordinate system and possibly project layer to a more appropriate projection """
    if arcpy.Describe(hazard_path).spatialReference.factoryCode != floodplain_ref.factoryCode: # evaluates if hazard coordinate system is different to floodplain coordinate system
        projected_hazard = NRI_GDB+fr"\{new_hazard_file}"
        arcpy.Project_management(hazard_path, new_hazard_file, floodplain_ref)
        # print(f"{new_hazard_file} has been projected")
    # else:
    #     print(f"{new_hazard_file} DID NOT need projection")
    in_features = [Floodplain_Data, projected_hazard]
    arcpy.management.RepairGeometry(Floodplain_Data)
    arcpy.management.RepairGeometry(projected_hazard)
    """ Overlapping function """
    # output_overlap = fr"Floodplain_{new_hazard_file}_Overlap"
    # arcpy.analysis.CountOverlappingFeatures(in_features, output_overlap,2)
    # print(f'{new_hazard_file} has been overlapped with Floodplain')
    """ Intersection function """
    output_intersect = fr"Floodplain_{new_hazard_file}_Intersect"
    arcpy.analysis.Intersect(in_features,output_intersect,"ALL")
    print(f'{new_hazard_file} has been intersected with Floodplain')