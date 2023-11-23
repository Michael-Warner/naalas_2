import arcpy

# Set up the environment
arcpy.env.workspace = r'C:\Users\warne\Desktop\Projects\naalas_2\Data\Table_Exports'  # Replace with your workspace path

# The path to your input table
input_table = 'ExtractValuesToTable1'  # Replace with your table name

# Read the table into a list of dictionaries
data = [row for row in arcpy.da.SearchCursor(input_table, ['OID', 'Value', 'SrcID_Feat', 'SrcID_Rast'])]

# Prepare the new wide format data structure
wide_data = {}
for row in data:
    oid_group = (row[0] - 1) // 10  # Group by OID, each group has 10 OIDs
    if oid_group not in wide_data:
        wide_data[oid_group] = []
    wide_data[oid_group].append(row)

# Define the output table
output_table = 'wide_format_table'  # Replace with your desired output table name
arcpy.CreateTable_management(arcpy.env.workspace, output_table)
arcpy.AddField_management(output_table, 'Group', 'LONG')

# Determine the number of fields based on the maximum group index
max_oid_group = max(wide_data.keys())
number_of_fields = max_oid_group + 1  # Including the 'Group' field

# Add fields for each of the OID groups
for i in range(number_of_fields - 1):  # Subtracting one because we already added the 'Group' field
    field_name = f'OID_Group_{i}'
    arcpy.AddField_management(output_table, field_name, 'TEXT')

# Define the field names for insertion
field_names = ['Group'] + [f'OID_Group_{i}' for i in range(number_of_fields - 1)]

# Insert the wide format data into the new table
with arcpy.da.InsertCursor(output_table, field_names) as cursor:
    for group, rows in wide_data.items():
        try:
            # Initialize the new row with empty strings for all fields
            new_row = ['' for _ in range(number_of_fields)]
            new_row[0] = group  # Set the group ID
            # Concatenate the row values into the corresponding group field, ensuring we don't exceed the number of fields
            for index, row in enumerate(rows):
                if index < number_of_fields - 1:  # Ensure the index is within the range of new_row
                    new_row[index + 1] = '; '.join(map(str, row))  # Adjust index by 1 to account for the 'Group' field
                else:
                    break  # Exit loop if there are more rows than fields to prevent IndexError
            # Insert the new row
            cursor.insertRow(new_row)
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Group: {group}, Row: {new_row}")

print(f"Wide format table '{output_table}' created successfully.")
