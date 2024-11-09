# import os
import pandas as pd
import geopandas as gpd
# import matplotlib

""" Folder path for datasets """
data_folder_path = r'/Users/javiermendez/Documents/Classes/Fall2024/GEOG 392/Project Data'
data_output_folder = data_folder_path+r'/Data_Output'
""" Houston Irradiance/Albido CSV files """
HoustonIrrAlbFolder = data_folder_path+r'/HoustonIrradianceAlbido_Tables'
Houston_Area = HoustonIrrAlbFolder+r"/POWER_Regional_Monthly_2012_2022.csv"

def row_to_list(alias, row_list):
   """ Will take field name alias and the list containing values. 
   Output will be a list of the row and its values """
   values_list = [] # this blank list will have the comma-separated values appended, this list will be the value of each row dictionary
   for item in range(len(row_list)):
      if item == 0: # locates the field name index, then replaces field name with alias as first list value
         values_list.append(alias)
      else: # all other values
         try:
            if item >= 4: # this index is where the data values for each month is found
               values_list.append(float(row_list[item])) # convert value to a numerical value
            else:
               values_list.append(row_list[item]) # indices before the monthly values
         except ValueError: # accounts for index identifier columns
            values_list.append(row_list[item])
   else:
      return values_list

def column_to_dict(ID, dict_list):
   """ Will input the column ID (same index for every row) and will iterate thru the list of dictionaries and create a new dictionary 
   with the column identifier as the index and the rest of the values for that particular row index into the list of values """
   new_list = [] # list of column values
   for dictionary in range(len(dict_list)): # iterates thru each index of the dictionary
      if dictionary == 0: # index for the first dictionary list (with column identifiers)
         column_name = dict_list[dictionary][ID] # the index for the new dictionary
      else:
         new_list.append(dict_list[dictionary][ID]) # value(s) for the new dictionary
   else:
      new_dict = {column_name:new_list} # new dictionary
      return new_dict

""" load data into GeoDataFrame """
# Downtown_readcsv = gpd.read_file(Downtown) # Latitude:29.7588 :: Longitude:-95.3709
# NE_Outer_readcsv = gpd.read_file(NE_Outer) # Latitude:30.055 :: Longitude:-95.0327
# NW_Outer_readcsv = gpd.read_file(NW_Outer) # Latitude:30.0498 :: Longitude:-95.7514
# SE_Outer_readcsv = gpd.read_file(SE_Outer) # Latitude:29.4749 :: Longitude:-95.028
# SW_Outer_readcsv = gpd.read_file(SW_Outer) # Latitude:29.4757 :: Longitude:-95.7752
HoustonArea_readcsv = gpd.read_file(Houston_Area) # Spatial Coordinate extent - Latitudes:29-31 :: Longitudes:-94.5 - -96.5
""" Preferred Soatial extent - Latitudes:29.5-30.1 :: Longitudes:-95 - -95.8 """

""" preview data """
# print(HoustonArea_readcsv.shape)
# print(HoustonArea_readcsv.columns)
# print(HoustonArea_readcsv.head())
# print(HoustonArea_readcsv.dtypes)
# print(HoustonArea_readcsv['-BEGIN'])
# HoustonArea_readcsv.plot()

""" The following variables are Field Aliases for their respective field name """
ALLSKY_SRF_ALB = 'All Sky Surface Albedo (dimensionless)'
ALLSKY_SFC_LW_DWN = 'All Sky Surface Longwave Downward Irradiance (W/m^2)'
ALLSKY_SFC_SW_DWN = 'All Sky Surface Shortwave Downward Irradiance (kW-hr/m^2/day)'
ALLSKY_SFC_PAR_TOT = 'All Sky Surface PAR Total (W/m^2)'
""" The following variables are the four different field dictionary lists """
row_values_list = []
""" The following variables count the loop iterations over the data for a specific field. 
Will be used as an ID to identify each dictionary's rows """
""" The first column of the dataset(s) contains rows with the relevant data as a comma-separated list of months/titles/values """
data_column = HoustonArea_readcsv['-BEGIN'] # '-BEGIN' is the column where the datavalues can be found
""" This loop will iterate thru the index values of the Houston Area csv dataset 
to query the correct rows for their name and lat/lon extent """
for row_ind in range(len(data_column)): # finds index in range of data column rows
   """ all rows after the 11th row contain the comma-separated values, but 
   the first row identifies each index in the row (year,lat,lon,month,etc.) """
   if (row_ind >= 11):
      new_list = data_column[row_ind].split(',') # creates a list of the current row
      """ Query thru the row values to find latitude and longitude, query for the values to 
      be within the desired spatial extent, then add the query results to a dictionary """
      try: # will test if the relevant indices are numerical and the right data (lat/lon)
         lat = float(new_list[2]) # the third index provides the latitude
         lon = float(new_list[3]) # the fourth index provides the longitude
      except ValueError:
         """ This exception will account for the first query row, which is the row index identifier """
         dictionary_title = row_to_list('FIELD', new_list)
         """ Append the row index identifier to each field dictionary before the values are added """
         row_values_list.append(dictionary_title)
         continue
      if (lat >= 29.5) and (lat <= 30.1) and (lon >= -95.8) and (lon <= -95): # desired spatial extent query
         """ Identifies the field name, and then creates a list of values, replacing 
         the field name with the field alias, then appends new list to the dictionary """
         if new_list[0] == 'ALLSKY_SRF_ALB':
            row_dict = row_to_list(ALLSKY_SRF_ALB, new_list)
            row_values_list.append(row_dict)
         elif new_list[0] == 'ALLSKY_SFC_LW_DWN':
            row_dict = row_to_list(ALLSKY_SFC_LW_DWN, new_list)
            row_values_list.append(row_dict)
         elif new_list[0] == 'ALLSKY_SFC_SW_DWN':
            row_dict = row_to_list(ALLSKY_SFC_SW_DWN, new_list)
            row_values_list.append(row_dict)
         elif new_list[0] == 'ALLSKY_SFC_PAR_TOT':
            row_dict = row_to_list(ALLSKY_SFC_PAR_TOT, new_list)
            row_values_list.append(row_dict)
else:
   Houston_dict_list = {} # will contain the dictionary of every field in the dataset
   """ Create the dictionary for each column, then append the dictionary to the large dictionary """
   FIELD_list = column_to_dict(0, row_values_list)
   Houston_dict_list.update(FIELD_list)
   YEAR_list = column_to_dict(1, row_values_list)
   Houston_dict_list.update(YEAR_list)
   LAT_list = column_to_dict(2, row_values_list)
   Houston_dict_list.update(LAT_list)
   LON_list = column_to_dict(3, row_values_list)
   Houston_dict_list.update(LON_list)
   JAN_list = column_to_dict(4, row_values_list)
   Houston_dict_list.update(JAN_list)
   FEB_list = column_to_dict(5, row_values_list)
   Houston_dict_list.update(FEB_list)
   MAR_list = column_to_dict(6, row_values_list)
   Houston_dict_list.update(MAR_list)
   APR_list = column_to_dict(7, row_values_list)
   Houston_dict_list.update(APR_list)
   MAY_list = column_to_dict(8, row_values_list)
   Houston_dict_list.update(MAY_list)
   JUN_list = column_to_dict(9, row_values_list)
   Houston_dict_list.update(JUN_list)
   JUL_list = column_to_dict(10, row_values_list)
   Houston_dict_list.update(JUL_list)
   AUG_list = column_to_dict(11, row_values_list)
   Houston_dict_list.update(AUG_list)
   SEP_list = column_to_dict(12, row_values_list)
   Houston_dict_list.update(SEP_list)
   OCT_list = column_to_dict(13, row_values_list)
   Houston_dict_list.update(OCT_list)
   NOV_list = column_to_dict(14, row_values_list)
   Houston_dict_list.update(NOV_list)
   DEC_list = column_to_dict(15, row_values_list)
   Houston_dict_list.update(DEC_list)
   ANN_list = column_to_dict(16, row_values_list)
   Houston_dict_list.update(ANN_list)
   """ Create a dataframe of the Listed Dictionary, then convert the dataframe to a new csv file """
   Houston_df = pd.DataFrame(Houston_dict_list)
   # Houston_df.to_csv(data_output_folder+'/Houston_Irradiance_Albido.csv')
   print(Houston_df)