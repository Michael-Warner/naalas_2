import arcpy
import math

# Set up the environment
arcpy.env.workspace = r'C:\Users\warne\Desktop\Projects\naalas_2\Data\Table_Exports'

# The path to your input table
input_table = 'ExtractValuesToTable1'

# Determine the number of columns for the wide table
count = int(arcpy.GetCount_management(input_table)[0])
number_of_columns = math.ceil(count / 10)

# Create the output table
output_table = 'wide_format_table'
arcpy.CreateTable_management(arcpy.env.workspace, output_table)

# Add the 'Value' columns to the output table
for i in range(number_of_columns):
    arcpy.AddField_management(output_table, f'Value{i}', 'LONG')

# Read the 'Value' column from the input table
values = [row[0] for row in arcpy.da.SearchCursor(input_table, ['Value'])]

# Group every 10 values into a list
value_columns = [values[i:i + 10] for i in range(0, len(values), 10)]

# Insert the grouped data into the new table
with arcpy.da.InsertCursor(output_table, [f'Value{i}' for i in range(number_of_columns)]) as cursor:
    # Since the number of values in each group may vary, initialize all to None
    row_template = [None] * number_of_columns
    for group in value_columns:
        # Create a new row based on the template and update with the current group values
        new_row = row_template[:]
        new_row[:len(group)] = group
        cursor.insertRow(new_row)

print(f"Wide format table '{output_table}' created successfully.")