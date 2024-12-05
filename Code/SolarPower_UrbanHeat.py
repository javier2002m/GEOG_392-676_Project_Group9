import arcpy

""" Data Folder Paths """
INPUT_DATA_PATH = r"\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-857847\Downloads\Project data"
OUTPUT_DATA_PATH = INPUT_DATA_PATH+r"\New_Data"

""" Set workspace to SolarPower.gdb where the buffer for each solar power attribute will be saved """
SolarPower_GDB = OUTPUT_DATA_PATH+r"\SolarPower.gdb"
arcpy.env.workspace = SolarPower_GDB
""" Path to solar power dataset and a list of solar power shapefile names """
SolarPower_Data = SolarPower_GDB+r"\Solar_Power_"
SolarPower_list = ["Albedo", "LongwaveIrradiance", "ShortwaveIrradiance", "PhotosyntheticActiveRadiation"] # Name of each sub dataset (attribute of solar power)

""" Create Buffer Analysis Shapefiles """
# I used ArcGIS Pro to estimate the horizontal and vertical distance between each solar power data point, and used the shortest distance to calculate a buffer radius
for solar in SolarPower_list: # iterates through the attribute sub dataset name for solar power
    """ The Solar Power grid of data points are about 7600 meters horizontally apart. 
    We use half that distance as the radius of each buffer to create a "buffer grid". """
    arcpy.Buffer_analysis(fr"{SolarPower_Data}{solar}", f"SolarPower{solar}Buffer", "3800 meter")

""" Path to Urban Heat Island dataset and a list of urban heat daytime names """
UrbanHeatIsland_data_folder = INPUT_DATA_PATH+r"\UrbanHeatIslands_HarrisCounty\Daytime_shp"
HeatIsland_daytime = ["Morning", "Afternoon", "Evening"] # Name of each sub dataset for heat island (daytime attribute)

""" Create Intersect GDB """
arcpy.management.CreateFileGDB(OUTPUT_DATA_PATH, "HeatIsland_SolarPower_Analysis.gdb") # Create a new geodatabase for the Solar Power Dataset
Heat_Solar_GDB = OUTPUT_DATA_PATH+r"\HeatIsland_SolarPower_Analysis.gdb" # Path to new gdb

""" Test differences in Spatial Reference for Urban Heat and Solar Power dataset """
for daytime in HeatIsland_daytime:
    daytime_HeatIsland = UrbanHeatIsland_data_folder+fr"\{daytime}\{daytime}_UrbanHeatIsland.shp" # path to iterated hazard list item
    HeatIsland_ref = arcpy.Describe(daytime_HeatIsland).spatialReference
    for solar in SolarPower_list:
        in_solar = SolarPower_GDB+fr"\SolarPower{solar}Buffer" # Path to currently iterated Solar Power Buffer
        """ Determine coordinate system and possibly project layer to a more appropriate projection """
        solar_projected = in_solar # path name of the solar power buffer BEFORE/WITHOUT projection
        try:
            # evaluates if Solar Power Buffer coordinate system is different to HeatIsland coordinate system
            if arcpy.Describe(in_solar).spatialReference.factoryCode != HeatIsland_ref.factoryCode:
                arcpy.Project_management(in_solar, solar+"_Projected", HeatIsland_ref)
                solar_projected = SolarPower_GDB+fr"\{solar}_Projected" # path name of the solar power buffer AFTER projection
                print(f"{solar} has been projected")
            else:
                print(f"{solar} DID NOT need projection")
        except:
            print(f"{solar} projection already exists")
        in_features = [daytime_HeatIsland, solar_projected] # Current iterated Heat Island daytime dataset and Solar Power buffer
        arcpy.env.workspace = Heat_Solar_GDB # Set Work Environment to Intersect results GDB
        """ Intersection function """
        output_intersect = fr"{daytime}_{solar}_Intersect" # name of the Intersect Result
        arcpy.analysis.Intersect(in_features,output_intersect)
        print(f'{solar} has been intersected with {daytime} Heat Island')