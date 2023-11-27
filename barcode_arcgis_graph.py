import arcpy
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Set the workspace
arcpy.env.workspace = r'C:\Users\warne\Desktop\Projects\naalas_2\Data\Table_Exports'

# Table name
table_name = 'wide_format_table'

# Convert the table to a pandas DataFrame
arr = arcpy.da.TableToNumPyArray(table_name, [field.name for field in arcpy.ListFields(table_name)])
df = pd.DataFrame(arr)

# Drop the first column
df = df.drop(columns="OID")

# Creating the heatmap
plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(df, annot=True, cmap='viridis', vmin=1, vmax=5)
plt.title('Heatmap of wide_format_table')

# Set up y-axis labels
y_labels = ['120 M', '90 M', '60 M', '30 M', 'Naala', '30 M', "60 M", "90 M", "120 M"]
heatmap.set_yticklabels(y_labels, rotation=0)  # Set the custom labels

# Set up x-axis labels
num_columns = df.shape[1]  # Number of columns in the DataFrame
tick_positions = np.arange(0, num_columns, 2)  # Tick positions for every other column
x_labels = [f'{60 * i} M' for i in range((num_columns + 1) // 2)]  # Labels for every other column

# Set the custom labels and positions
heatmap.set_xticks(tick_positions)
heatmap.set_xticklabels(x_labels, rotation=45)

plt.show()

# If you need to save the plot
# plt.savefig(r'C:\path\to\save\heatmap.png')
