import pandas as pd
import plotly.graph_objects as go

# Load the CSV file
file_path = 'data/data-copyleft.csv'  # Adjust this to your file's location
data = pd.read_csv(file_path)

# Step 1: Calculate total packages and percentages
total_per_type = data.groupby("Type")["Packages"].sum().reset_index()
total_per_type.columns = ["Type", "Total"]

# Merge totals into the original data to calculate percentages
data = data.merge(total_per_type, on="Type")
data["Percentage"] = (data["Packages"] / data["Total"] * 100).round(1)

# Step 2: Pivot the data to format it for Plotly Table
pivot_packages = data.pivot_table(index=["Type", "SPDX_ID"], columns="LOB", values="Packages", fill_value=0)

# Step 3: Combine totals and percentages into a single dataset for display
rows = []
row_colors = []  # Row-wise background colors

for type_, group in pivot_packages.groupby(level=0):
    # Add header row for "Strong copyleft" and "Weak copyleft"
    rows.append(["<b>" + type_ + "</b>"] + list(group.sum().values))
    row_colors.append("#F5F5F5")  # Light gray for copyleft rows
    
    # Add SPDX breakdown rows
    for (type_, spdx_id), row in group.iterrows():
        percentages = list(((row.values / group.sum().values) * 100).round(1))
        percentages_with_symbol = [f"{value}%" for value in percentages]
        rows.append(["<b>" + spdx_id + "</b>"] + percentages_with_symbol)
        row_colors.append("white")  # Default color for SPDX_ID rows

# Convert rows to DataFrame
headers = ["Type/SPDX_ID"] + list(pivot_packages.columns)
final_table = pd.DataFrame(rows, columns=headers)

# Step 4: Generate Colors for the Table
cell_colors = []
for col in final_table.columns[1:]:
    col_colors = []
    for val in final_table[col]:
        # Apply traffic light coloring for percentage cells
        if isinstance(val, str) and "%" in val:
            percentage = float(val.strip('%'))
            if percentage < 10:
                col_colors.append("green")
            elif 10 <= percentage < 25:
                col_colors.append("yellow")
            else:
                col_colors.append("red")
        else:
            col_colors.append("#F5F5F5")  # Light gray for non-percentage cells
    cell_colors.append(col_colors)

# Apply row-wise colors for the first column
first_column_colors = row_colors

# Step 5: Create the Plotly table
fig = go.Figure(
    data=[
        go.Table(
            header=dict(
                values=["<b>" + col + "</b>" for col in final_table.columns],
                fill_color="#A9A9A9",  # Darker gray for header
                align="center",
                font=dict(size=12, color="white"),
            ),
            cells=dict(
                values=[ final_table[col] for col in final_table.columns],
                fill_color=[first_column_colors] + cell_colors,  # Apply traffic light and row colors
                align="center",
                font=dict(size=11, color="black"),
            ),
        )
    ]
)

# Add annotations/footnotes for the color legend
fig.add_annotation(
    text="<b>Color Legend:</b><br>"
         "<span >Green</span>: <10% | "
         "<span >Yellow</span>: 10%-25% | "
         "<span >Red</span>: >25%",
    x=0.5,
    y=-0.15,  # Adjust position below the table
    xref="paper",
    yref="paper",
    showarrow=False,
    align="center",
    font=dict(size=12, color="black"),
    bgcolor="white",
    bordercolor="black",
)

# Update layout for better display
fig.update_layout(
    title="Strong Copyleft vs Weak Copyleft with Percentages",
    title_x=0.5,
    width=1200,
    height=470,  # Increased height for the footnote
)

# Show the Plotly figure
fig.show()
