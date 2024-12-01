import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
file_path = 'data/data.csv'  # Replace with your actual data file path

# Clean column names to remove leading/trailing spaces
data.columns = data.columns.str.strip()

# Calculate the percentage of affected seals
data['% Effected'] = (data['Effected_Seals'] / data['Seals']) * 100

# Create a custom label for each LOB to show total seals and % affected (centered text)
data['Label'] = (
    '<b>' + data['LOB'] + '</b><br>Total Seals: ' + data['Seals'].astype(str) +
    '<br>% Effected: ' + data['% Effected'].round(2).astype(str) + '%'
)

# Create custom hover text
data['Hover'] = (
    'LOB: ' + data['LOB'] +
    '<br>Total Seals: ' + data['Seals'].astype(str) +
    '<br>Effected Seals: ' + data['Effected_Seals'].astype(str) +
    '<br>% Effected: ' + data['% Effected'].round(2).astype(str) + '%'
)

# Create a treemap using plotly.graph_objects
fig = go.Figure(
    go.Treemap(
        labels=data['Label'],  # Custom labels with bold LOB name
        parents=[""] * len(data),  # No hierarchical structure
        values=data['Seals'],  # Size of each block
        marker=dict(
            #colors=data['Seals'] * data['Effected_Seals'],  # Color based on combined metric
            colors=data['% Effected'],
            colorscale='RdYlGn',  # Red-to-green color scale
            reversescale=True,  # Reverse scale: green for high, red for low
            showscale=True  # Show the color bar
        ),
        hovertext=data['Hover'],  # Custom hover text
        hoverinfo='text',  # Use the custom hover text
        textinfo='label',  # Display only the label on blocks
        textposition='middle center'  # Center the text within each block
    )
)

# Update layout
fig.update_layout(
    title="Treemap of Seals and Effected Seals by LOB (Centered Label + Custom Hover)"
)

# Show the plot
fig.show()
