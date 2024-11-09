# import os
import pandas as pd
import geopandas as gpd
# import matplotlib

def Dataframe_to_list(object):
   """Converts  a dataframe or geodatabase table to an iterable list. 
   Input is the dataframe/table, and output is assigning a the list to a variable"""
   new_list = []
   for item in object:
      try: # Iterate thru dataframe items and test whether item is a number
         new_list.append(round(float(item),2)) # rounds decimal numbers to the hundredth place
      except ValueError: # continue to append values/names/dictionaries
         new_list.append(item)
   else:
      return new_list # the output list

def dictionary_append(dictionary_list, ID):
   """Function that appends wanted/needed rows of values from the NRI Data Dictionary file, 
   and organizes data into a descriptive and smaller extent. 'dictionary_list' is a list 
   full of rows (new_list's), so each index in the dictionary is a new row/list"""
   new_list = [] # New row
   new_list.append(ID+1) # Adds ID value, and adjusts to its original value (a 1 is subtracted from original value later)
   new_list.append(NRI_DICTNames[ID]) # Field Name for the specific list ID
   new_list.append(NRI_DICTAlias[ID]) # Field Alias for the specific list ID
   new_list.append(NRI_DICTLayers[ID]) # Relevant Layer name for the specific list ID
   new_list.append(NRI_DICTtype[ID]) # Metric Type name for the specific list ID
   dictionary_list.append(new_list) # Appends row to dictionary

def FieldValues_ToNewDictionary(alias, values):
   """ Function will take a given name/title for the list of values and will 
   then create a dictionary between a the title and the list of values as output"""
   new_list = []
   for x in values:
      new_list.append(x)
   else:
      new_dict = {alias:new_list}
      return new_dict

""" Folder path for datasets """
data_folder_path = r'/Users/javiermendez/Documents/Classes/Fall2024/GEOG 392/Project Data'
data_output_folder = data_folder_path+r'/Data_Output'
""" NRI Table Census Tracts in Texas """
NRI_path = data_folder_path+r'/NRI_Table_CensusTracts_Texas'
NRI_csv = NRI_path+r'/NRI_Table_CensusTracts_Texas.csv'
NRI_dict = NRI_path+r'/NRIDataDictionary.csv'
""" load data into GeoDataFrame """
nri_csv_readfile = gpd.read_file(NRI_csv)
nri_dict_readfile = gpd.read_file(NRI_dict)

""" preview data """
# print(nri_csv_readfile.shape)
# print(nri_dict_readfile.shape)
# print(nri_csv_readfile.head(0))  # Dictionary readfile has 479 rows
# print(nri_dict_readfile.head())  # Dictionary readfile has 479 rows
# print(nri_csv__readfile.columns)
# print(nri_dict__readfile.columns)
# print(nri_csv__readfile.dtypes)
# print(nri_dict__readfile.dtypes)
# nri_csv__readfile.plot()

""" Table of Fields/Columns from the NRI CSV dataset """
NRI_CSVfields = Dataframe_to_list(nri_csv_readfile.columns)

""" Table of field IDs for the NRI CSV dataset, from the dictionary list """
NRI_DICTid = Dataframe_to_list(nri_dict_readfile['Sort'])
""" Table of field NAMES for the NRI CSV dataset, from the dictionary list """
NRI_DICTNames = Dataframe_to_list(nri_dict_readfile['Field Name'])
""" Table of field ALIASES for the NRI CSV dataset, from the dictionary list """
NRI_DICTAlias = Dataframe_to_list(nri_dict_readfile['Field Alias'])
""" Table of field LAYERS for the NRI CSV dataset, from the dictionary list """
NRI_DICTLayers = Dataframe_to_list(nri_dict_readfile['Relevant Layer'])
""" Table of field TYPEs for the NRI CSV dataset, from the dictionary list """
NRI_DICTtype = Dataframe_to_list(nri_dict_readfile['Metric Type'])

""" Loops trhu NRI IDs, calls ID from the table to append relevant information to new NRI Dictionary File """
dictionary_params = [] # List of dictionary layer parameters
for dict_index in NRI_DICTid:
   field_index = int(dict_index)-1 # the first value of NRI_DICTid (index 0) is 1, so we subtract a 1 to start from 0
   """ Will extract the identifier fields with object ID, shape, etc. """
   if NRI_DICTLayers[field_index] == 'n/a':
      dictionary_append(dictionary_params, field_index)
   """ Extract IDs 5,6,8,12,14,15,18 """
   if (int(dict_index) == 5) or (int(dict_index) == 6) or (int(dict_index) == 8) or (int(dict_index) == 12) or (int(dict_index) == 14) or (int(dict_index) == 15) or (int(dict_index) == 18):
      dictionary_append(dictionary_params, field_index)
   # elif NRI_DICTLayers[x] == 'Social Vulnerability and Community Resilience Adjusted Expected Annual Loss Rate':
   #    dictionary_append(dictionary_params, field_index)
   # elif NRI_DICTLayers[x] == 'Social Vulnerability' and (NRI_DICTtype[x] == 'State Percentile'):
   #    dictionary_append(dictionary_params, field_index)
   # elif NRI_DICTLayers[x] == 'Community Resilience' and (NRI_DICTtype[x] == 'State Percentile'):
   #    dictionary_append(dictionary_params, field_index)
   """ This portion will add this dictionary data to a hazard dictionary list """
   hazard_parameters = (NRI_DICTtype[field_index] == 'Number of Events') or (NRI_DICTtype[field_index] == 'Annualized Frequency') or (NRI_DICTtype[field_index] == 'National Percentile')
   if NRI_DICTLayers[field_index] == 'Coastal Flooding' and hazard_parameters:
      dictionary_append(dictionary_params, field_index)
   elif NRI_DICTLayers[field_index] == 'Drought' and hazard_parameters:
      dictionary_append(dictionary_params, field_index)
   elif NRI_DICTLayers[field_index] == 'Heat Wave' and hazard_parameters:
      dictionary_append(dictionary_params, field_index)
   elif NRI_DICTLayers[field_index] == 'Hurricane' and hazard_parameters:
      dictionary_append(dictionary_params, field_index)
   elif NRI_DICTLayers[field_index] == 'Riverine Flooding' and hazard_parameters:
      dictionary_append(dictionary_params, field_index)
   # elif NRI_DICTLayers[x] == 'Landslide':
      # dictionary_append(dictionary_params, field_index)

""" Will iterate thru a list of indices of the County names field in the NRI CSV dataset
with the goal of finding the first and last COUNTY index values for Harris county """
counties = Dataframe_to_list(nri_csv_readfile['COUNTY']) # List of county names
harris_range = [] # a list that will hold all the indices in the list of counties
for id in range(len(counties)):
   if counties[id] == 'Harris':
      harris_range.append(id)
""" Now we have the range of indices which queries the data to be in Harris county """
harris_co_range = range(harris_range[0],harris_range[-1]+1) # add a 1 so the range of indices ends on the desired range value

""" Will store several lists of dictionaries, each containing the data values 
within the spatial extent of Harris County for their respective fields/layers. 
This list of dictionaries is the result of the spatial query for Harris County 
and the conditions of the hazard layers we ascribed importance to, 
which will be used to write the output CSV """
csv_new_dict_list = {}

""" Start searching for relevant columns in the NRI CSV file and 
copy the data values from the dataset to a listed dictionary """
for csv_field in NRI_CSVfields: # Loops thru list of NRI CSV fields
   for param_index in range(len(dictionary_params)): # Loops thru an indexed range of the Dictionary Parameters queried
      relevant_name = dictionary_params[param_index][1] # Field Name # Matches NRI CSV Field name with the ®elevant alias
      relevant_alias = dictionary_params[param_index][2] # Field Alias # Gives list with more descriptive Name/Title
      relevant_layer = dictionary_params[param_index][3] # Relevant Layer # Identifies which hazard layer it belongs to
      relevant_metric = dictionary_params[param_index][4] # Metric Type # Identifies which Hazard parameter is being selected/created
      csv_values = nri_csv_readfile[csv_field][harris_co_range] # A dataframe of values in the specified field name, within the 'Harris county' range of values
      RelevantField_ValuesList = Dataframe_to_list(csv_values) # list of values from the specified field and value range
      """ Now that we have the field name in the original dataset, its list of values, and range of values, 
      then the name for the new list (alias), the target layer (relevant), and the metric type we can create 
      our own list with the fields and values we want """
      if csv_field == relevant_name:
         """ 'csv_field == relevant_name' Should only occur when mathing CSV field name with 
         Dictionary Field Name, to then add field alias as the dictionary title/index to its values """
         layer_dictionary = FieldValues_ToNewDictionary(relevant_alias,RelevantField_ValuesList)
         csv_new_dict_list.update(layer_dictionary)
      else: # Appends 'OID_' but excludes all other fields
         if csv_field == 'OID_':
            id_list = FieldValues_ToNewDictionary('NRI_ObjectID',RelevantField_ValuesList)
            csv_new_dict_list.update(id_list)
            break
# print(csv_new_dict_list)

df = pd.DataFrame(csv_new_dict_list)
# df.to_csv(data_output_folder+'/NRI_CensusTracts_HarrisCO.csv')