import arcpy
import math

# Set up the environment
arcpy.env.workspace = r'C:\Users\warne\Desktop\Projects\naalas_2\Data\Table_Exports'

# The path to your input table
input_table = 'ExtractValuesToTable1'

# Determine the number of columns for the wide table based on the count of rows in the input table
count = int(arcpy.GetCount_management(input_table).getOutput(0))
number_of_columns = math.ceil(count / 10)

# Create the output table
output_table = 'wide_format_table'
arcpy.CreateTable_management(arcpy.env.workspace, output_table)

# Add the 'Value' columns to the output table
for i in range(number_of_columns):
    arcpy.AddField_management(output_table, f'Value{i}', 'LONG')

# Read the 'Value' column from the input table
values = [row[0] for row in arcpy.da.SearchCursor(input_table, ['Value'])]

# Group every 10 values into a list, padding with None if necessary
value_columns = [values[i:i + 10] + [None]*(10 - len(values[i:i + 10])) for i in range(0, len(values), 10)]

# Define the field names for insertion based on the number of columns
field_names = [f'Value{i}' for i in range(number_of_columns)]

# Insert the grouped data into the new table
with arcpy.da.InsertCursor(output_table, field_names) as cursor:
    # Transpose the value columns to rows
    for row in zip(*value_columns):
        # Replace 'None' with a placeholder if necessary, for example, use 0 or ''
        # row = [0 if v is None else v for v in row]
        cursor.insertRow(row)

print(f"Wide format table '{output_table}' created successfully.")



import arcpy

# Set up the environment
arcpy.env.workspace = r'C:\Users\warne\Desktop\Projects\naalas_2\Data\Table_Exports'

# The path to your output table
output_table = 'wide_format_table'

# Define the field names for insertion based on the existing fields in the table
# This assumes the fields are named 'Value0', 'Value1', ..., 'ValueN'
# Adjust the range according to the actual number of value fields in your table
field_names = [f'Value{i}' for i in range(10)]  # Adjust the range as necessary

# The data to be inserted - a single row with ten integer values
# Ensure this matches the number of Value fields you have in your output table
row_data = tuple(range(10))  # Example row data: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

# Insert a single row of data into the new table
with arcpy.da.InsertCursor(output_table, field_names) as cursor:
    cursor.insertRow(row_data)

print(f"Single row inserted into '{output_table}' successfully.")


import arcpy

# Set up the environment
arcpy.env.workspace = r'C:\Users\warne\Desktop\Projects\naalas_2\Data\Table_Exports'

# The name of your input table
input_table = 'ExtractValuesToTable1'

# The name of your output table
output_table = 'wide_format_table'

# Check if the output table already exists, delete it if it does
if arcpy.Exists(output_table):
    arcpy.Delete_management(output_table)

# Create the output table
arcpy.CreateTable_management(arcpy.env.workspace, output_table)

# Add the 'Value' column to the output table, assuming 'Value' is of type LONG
arcpy.AddField_management(output_table, 'Value', 'LONG')

# Insert the 'Value' column data from the input table to the output table
with arcpy.da.SearchCursor(input_table, ['Value']) as search_cursor, \
     arcpy.da.InsertCursor(output_table, ['Value']) as insert_cursor:
    for row in search_cursor:
        insert_cursor.insertRow(row)

print(f"'Value' column data transferred to '{output_table}' successfully.")

reader = pd.read_csv('data.csv', sep=',', chunksize=10,
                       index_col=0, header=None, names=['Generation', 'Fitness'])

my_df = pd.concat((chunk for chunk in reader), axis=1)