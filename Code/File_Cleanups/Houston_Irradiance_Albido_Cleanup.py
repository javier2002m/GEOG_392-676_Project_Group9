# import os
import pandas as pd
import geopandas as gpd
# import matplotlib

""" Folder path for datasets """
data_folder_path = r'/Users/javiermendez/Documents/Classes/Fall2024/GEOG 392/Project Data'
data_output_path = data_folder_path+r'/Data_Output'
""" Houston Irradiance/Albido CSV files """
HoustonIrrAlbFolder = data_folder_path+r'/HoustonIrradianceAlbido_Tables'
# Houston_Area = HoustonIrrAlbFolder+r"/POWER_Regional_Monthly_2012_2022.csv"
DownloadedData_Folder = HoustonIrrAlbFolder+r'/108HoustonIrradAlbedo_Tables'
'/Users/javiermendez/Documents/Classes/Fall2024/GEOG 392/Project Data/HoustonIrradianceAlbido_Tables'

""" load data into GeoDataFrame """
# HoustonArea_readcsv = gpd.read_file(Houston_Area) # Spatial Coordinate extent - Latitudes:29-31 :: Longitudes:-94.5 - -96.5
""" Preferred Soatial extent - Latitudes:29.5-30.1 :: Longitudes:-95 - -95.8 """

""" preview data """
# print(Houston_CSV_Reader.shape)
# print(Houston_CSV_Reader.columns)
# print(Houston_CSV_Reader.head())
# print(Houston_CSV_Reader.dtypes)
# print(Houston_CSV_Reader['-BEGIN'])
# Houston_CSV_Reader.plot()

def row_to_list(row_list, alias, lat, lon):
   """ Will take field name alias and the list containing values. 
   Output will be a list of the row and its values """
   values_list = [] # this blank list will have the comma-separated values appended, this list will be the value of each row dictionary
   for item in range(len(row_list)):
      if item == 0: # locates the field name index, then replaces field name with alias as first list value
         values_list.append(alias)
      else: # all other values
         if item == 1:
            values_list.append(lat) # append lat value/identifier
            values_list.append(lon) # append lon value/identifier
            try: # try converting the current list item to a numeric value
               values_list.append(float(row_list[item])) # append first month (JAN)
            except ValueError: # unless the list item is an identifier value
               values_list.append(row_list[item])
         else: # all other values
            try: # try converting the current list item to a numeric value
               values_list.append(float(row_list[item]))
            except ValueError: # unless the list item is an identifier value
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


""" The following variables are Field Aliases for their respective field name """
ALLSKY_SRF_ALB = 'All Sky Surface Albedo (dimensionless)'
ALLSKY_SFC_LW_DWN = 'All Sky Surface Longwave Downward Irradiance (W/m^2)'
ALLSKY_SFC_SW_DWN = 'All Sky Surface Shortwave Downward Irradiance (kW-hr/m^2/day)'
ALLSKY_SFC_PAR_TOT = 'All Sky Surface PAR Total (W/m^2)'
""" The following list will store all the list of values of each iterated row """
row_values_list = [] # aka, large list of data values

lat_list = [29.5] # lowest latitude coordinate
while lat_list[-1] <= 30.1: # this loop while add 9 values before 30.1, the 
   lat_list.append(round((lat_list[-1]+0.07),2))
del lat_list[-1]
lat_iter = iter(lat_list)
lat = next(lat_iter)

lon_list = [-95] # lowest longitude coordinate
while lon_list[-1] >= -95.8:
   lon_list.append(round((lon_list[-1]-0.07),2))
del lon_list[-1]
lon_iter = iter(lon_list)
lon = next(lon_iter)

""" Number each csv, then write a for loop to iterate thru a list of numbers that will call the csv file """
for z in range(1,109): # iterates thru numbered list of csv data files
   # DownloadedData_Folder = r'/Users/javiermendez/Downloads/HoustonIrradAlbedo_Tables'
   # Houston_CSV_Reader = gpd.read_file(DownloadedData_Folder+r'/Houston1.csv')
   Houston_CSV_Reader = gpd.read_file(DownloadedData_Folder+r'/Houston'+str(z)+'.csv') # Spatial Coordinate extent - Latitudes:29-31 :: Longitudes:-94.5 - -96.5
   iter_csv_file = Houston_CSV_Reader['-BEGIN'] # calls the columns with values for each csv data file
   """ This loop should iterate thru the rows of values in each csv data file, add the values (alongside lat and lon) 
   to a temporary list and once complete add the list of the values to the large list of data values """
   for row_ind in range(len(iter_csv_file)): # iterates through the range of indices of the data column rows
      if z == 1: # identifies the first file to extract the value identifier row as the header of the dataframe
         """ The following code block and loop will extract the header list of values (value identifier row) 
         from the csv as a list, then append the list to the large list of data values """
         if row_ind == 11: # index of the value identifier row
            iter_row = iter_csv_file[row_ind].split(',') # creates a list of the value identifier row
            row_list = row_to_list(iter_row, 'FIELD', 'LAT', 'LON') # Inputs field, lat, and lon as headers for the fields, latitudes, and longitudes columns
            row_values_list.append(row_list)
      if row_ind > 11: # value rows after the identifier row
         iter_row = iter_csv_file[row_ind].split(',') # creates a list of the current row
         """ The following block of statements reads the field name for the row and inserts 
         a field alias, and latitude and longitude coordinates """
         if iter_row[0] == 'ALLSKY_SRF_ALB':
            row_list = row_to_list(iter_row, ALLSKY_SRF_ALB, lat, lon)
            row_values_list.append(row_list)
         elif iter_row[0] == 'ALLSKY_SFC_LW_DWN':
            row_list = row_to_list(iter_row, ALLSKY_SFC_LW_DWN, lat, lon)
            row_values_list.append(row_list)
         elif iter_row[0] == 'ALLSKY_SFC_SW_DWN':
            row_list = row_to_list(iter_row, ALLSKY_SFC_SW_DWN, lat, lon)
            row_values_list.append(row_list)
         elif iter_row[0] == 'ALLSKY_SFC_PAR_TOT':
            row_list = row_to_list(iter_row, ALLSKY_SFC_PAR_TOT, lat, lon)
            row_values_list.append(row_list)
   """ When z (file number) is 9, or every 9 files, the coordinates reset. 
   The next file coordinates start with the first latitude (29.5) and 
   continue to the next longtiude (-95 to -95.07) """
   if z == 108: # Finds last index
      break # breaks loop before error over iterator
   if z % 9 == 0: # Determines if 9 iterations of file have been read
      lon = next(lon_iter) # Next Longitude
      lat_iter = iter(lat_list) # Resets the iterating list of latitudes
      lat = next(lat_iter) # First latitude of reset
   else: # Within the 9-file iterations
      lat = next(lat_iter) # Next Latitude

Houston_dict_list = {} # will contain the dictionary of every field in the dataset
""" Create the dictionary for each dataframe column, then append the dictionary to the large dictionary """
FIELD_dict = column_to_dict(0, row_values_list)
Houston_dict_list.update(FIELD_dict)
LAT_dict = column_to_dict(1, row_values_list)
Houston_dict_list.update(LAT_dict)
LON_dict = column_to_dict(2, row_values_list)
Houston_dict_list.update(LON_dict)
JAN_dict = column_to_dict(3, row_values_list)
Houston_dict_list.update(JAN_dict)
FEB_dict = column_to_dict(4, row_values_list)
Houston_dict_list.update(FEB_dict)
MAR_dict = column_to_dict(5, row_values_list)
Houston_dict_list.update(MAR_dict)
APR_dict = column_to_dict(6, row_values_list)
Houston_dict_list.update(APR_dict)
MAY_dict = column_to_dict(7, row_values_list)
Houston_dict_list.update(MAY_dict)
JUN_dict = column_to_dict(8, row_values_list)
Houston_dict_list.update(JUN_dict)
JUL_dict = column_to_dict(9, row_values_list)
Houston_dict_list.update(JUL_dict)
AUG_dict = column_to_dict(10, row_values_list)
Houston_dict_list.update(AUG_dict)
SEP_dict = column_to_dict(11, row_values_list)
Houston_dict_list.update(SEP_dict)
OCT_dict = column_to_dict(12, row_values_list)
Houston_dict_list.update(OCT_dict)
NOV_dict = column_to_dict(13, row_values_list)
Houston_dict_list.update(NOV_dict)
DEC_dict = column_to_dict(14, row_values_list)
Houston_dict_list.update(DEC_dict)
ANN_dict = column_to_dict(15, row_values_list)
Houston_dict_list.update(ANN_dict)
""" Create a dataframe of the Listed Dictionary, then convert the dataframe to a new csv file """
Houston_df = pd.DataFrame(Houston_dict_list)
print(Houston_df)
# Houston_df.to_csv(data_output_path+'/108Table_HoustonIrradianceAlbedo.csv')