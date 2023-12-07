import arcpy
import pandas as pd
import numpy as np

# Set up the environment
# EDIT THIS TO MATCH YOUR ENVIRONMENT
arcpy.env.workspace = r'C:\Users\warne\Desktop\Projects\naalas_2\Data\Table_Exports'

# The path to your input table
input_table = 'ExtractValuesToTable1'

# Convert the table to a pandas DataFrame
arr = arcpy.da.TableToNumPyArray(input_table, ['Value', 'SrcID_Feat'])
df = pd.DataFrame(arr)
df.fillna(0, inplace=True)

# Set the df in the proper ascending order
df = df.sort_values(by = "SrcID_Feat")

# Calculate the number of rows that would be in each column
# and the total number of such columns needed
rows_per_column = 10
num_columns = int(np.ceil(df.shape[0] / rows_per_column))

# Initialize a new DataFrame to store the reshaped data
reshaped_data = pd.DataFrame()

# Iterate to fill the new DataFrame
for i in range(num_columns):
    start_row = i * rows_per_column
    end_row = start_row + rows_per_column
    column_values = df['Value'][start_row:end_row].reset_index(drop=True)
    reshaped_data[f'Value_{i}'] = column_values

# When ArcGIS Pro creates transects based on every x meters it doesn't start with 
# the first pixel, but with the x meter from the start. 
# It then creates all the transects then goes back and creates the transect
# at the first pixel of the line then the last pixel of the line.

# This moves the second to last transect generated, to the "front" where it should be.

columns = list(reshaped_data.columns)

# Move the second to last column to the front
columns.insert(0, columns.pop(-2))  # -2 index is the second to last item

# Reindex the DataFrame with the new column order
reshaped_data = reshaped_data[columns]

# Drop the row with the double end points generated when creating Points on a line
reshaped_data = reshaped_data.drop([9])

# Write the DataFrame back to a new table
output_table = 'wide_format_table'
if arcpy.Exists(output_table):
    arcpy.Delete_management(output_table)
    
# Specify the path for the new table
output_path = arcpy.env.workspace + "\\" + output_table
# Use a pandas function to save DataFrame to a CSV, and then convert it to a table
csv_output = output_path + ".csv"
reshaped_data.to_csv(csv_output, index=False)
arcpy.TableToTable_conversion(csv_output, arcpy.env.workspace, output_table)

# Clean up the CSV file after creating the table
if arcpy.Exists(csv_output):
    arcpy.Delete_management(csv_output)

print(f"Dataframe exported to '{output_table}' successfully.")