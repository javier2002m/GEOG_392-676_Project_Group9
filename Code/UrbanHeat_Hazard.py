import arcpy
import os

""" Data Folder Paths """
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DATA_PATH = r"\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-857847\Downloads\Project data"
OUTPUT_DATA_Path = INPUT_DATA_PATH+r"\New_Data"

UrbanHeatIsland_data_folder = INPUT_DATA_PATH+r"\UrbanHeatIslands_HarrisCounty\Daytime_shp"
# \\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-857847\Downloads\Project data\UrbanHeatIslands_HarrisCounty\Daytime_shp
HeatIsland_daytime = ["Morning", "Afternoon", "Evening"]

NRI_GDB = OUTPUT_DATA_Path+r"\NRI_CensusTracts_Hazards_shp.gdb"
NRI_Hazards = NRI_GDB+r"\NRI_Shapefile_CensusTracts_HarrisCO"
Drought = NRI_GDB+r"\Drought_shp_NRI_CensusTracts_HarrisCo"
HeatWave = NRI_GDB+r"\HeatWave_shp_NRI_CensusTracts_HarrisCo"

# RiverineFlooding = NRI_GDB+r"\RiverineFlooding_shp_NRI_CensusTracts_HarrisCo"
# CoastalFlooding = NRI_GDB+r"\CoastalFlooding_shp_NRI_CensusTracts_HarrisCo"
# Hurricane = NRI_GDB+r"\Hurricane_shp_NRI_CensusTracts_HarrisCo"
""" List of hazard paths """
hazards_list = [HeatWave, Drought]
hazards_name = ["HeatWave", "Drought"]

""" Create GDB and setup workspace """
# arcpy.management.CreateFileGDB(OUTPUT_DATA_Path, "HeatIsland_Hazard_Analysis.gdb") # Create a new geodatabase for the Urban Heat Island and Hazards Dataset analysis
HeatIsland_GDB = OUTPUT_DATA_Path+r"\HeatIsland_Hazard_Analysis.gdb" # Path to new gdb
arcpy.env.workspace = HeatIsland_GDB # Set Work Environment to new gdb

# arcpy.management.XYTableToPoint(HeatIsland_file+fr"{daytime}.csv", fr"{daytime}_UrbanHeatIsland", 'LON', 'LAT') # create Urban Heat Island shapefile for current iterated daytime

""" Create Intersect layers of every dataset """
for daytime in HeatIsland_daytime:
    daytime_HeatIsland = UrbanHeatIsland_data_folder+fr"\{daytime}\{daytime}_UrbanHeatIsland.shp" # path to iterated hazard list item
    HeatIsland_ref = arcpy.Describe(daytime_HeatIsland).spatialReference
    # print(daytime_HeatIsland)
    # print(HeatIsland_ref)
    for hazard in range(len(hazards_list)):
        hazard_path = hazards_list[hazard] # folder path of the iterated hazard layer
        new_hazard_file = hazards_name[hazard] # could be the path name of the projected hazard layer
        projected_hazard = hazard_path
        # print(hazard_path)
        # print(new_hazard_file)
        """ Determine coordinate system and possibly project layer to a more appropriate projection """
        if arcpy.Describe(hazard_path).spatialReference.factoryCode != HeatIsland_ref.factoryCode: # evaluates if hazard coordinate system is different to floodplain coordinate system
            projected_hazard = HeatIsland_GDB+fr"\{new_hazard_file}_Projected" # path name of the projected hazard layer
            arcpy.Project_management(hazard_path, new_hazard_file+"_Projected", HeatIsland_ref)
            # print(f"{new_hazard_file} has been projected")
        # else:
        #     print(f"{new_hazard_file} DID NOT need projection")
        in_features = [daytime_HeatIsland, projected_hazard]
        arcpy.management.RepairGeometry(daytime_HeatIsland)
        arcpy.management.RepairGeometry(projected_hazard)
        """ Overlapping function """
        # output_overlap = fr"Floodplain_{new_hazard_file}_Overlap"
        # arcpy.analysis.CountOverlappingFeatures(in_features, output_overlap,2)
        # print(f'{new_hazard_file} has been overlapped with Floodplain')
        """ Intersection function """
        output_intersect = fr"{daytime}_{new_hazard_file}_Intersect"
        print(output_intersect)
        arcpy.analysis.Intersect(in_features,output_intersect)
        print(f'{new_hazard_file} has been intersected with {daytime} Heat Island')