import dash
from dash import dcc, html, dash_table
import pandas as pd
from dash.dash_table.Format import Format, Scheme, Group

# Load the provided data file
df = pd.read_csv('data_derived.csv')

# Aggregate data by 'lob' and calculate the sum of 'total_seals'
aggr_data = df.groupby("lob", as_index=False).agg({"total_seals": "sum"})

# Create new columns for 'derived_color' being 'Red', 'Yellow', and 'Green'
red_data = df[df['derived_color'] == 'Red'].groupby("lob", as_index=False).agg({"total_seals": "sum"})
yellow_data = df[df['derived_color'] == 'Yellow'].groupby("lob", as_index=False).agg({"total_seals": "sum"})
green_data = df[df['derived_color'] == 'Green'].groupby("lob", as_index=False).agg({"total_seals": "sum"})

aggr_data = aggr_data.merge(red_data, on="lob", how="left", suffixes=('', '_red'))
aggr_data = aggr_data.merge(yellow_data, on="lob", how="left", suffixes=('', '_yellow'))
aggr_data = aggr_data.merge(green_data, on="lob", how="left", suffixes=('', '_green'))

aggr_data["Red"] = aggr_data["total_seals_red"].fillna(0)
aggr_data["Yellow"] = aggr_data["total_seals_yellow"].fillna(0)
aggr_data["Green"] = aggr_data["total_seals_green"].fillna(0)

# Add percentage columns
aggr_data['Red %'] = ((aggr_data['Red'] / aggr_data['total_seals']) * 100).round(1)
aggr_data['Yellow %'] = ((aggr_data['Yellow'] / aggr_data['total_seals']) * 100).round(1)
aggr_data['Green %'] = ((aggr_data['Green'] / aggr_data['total_seals']) * 100).round(1)

# Normalize values for coloring
def normalize(value, min_val, max_val):
    if max_val > min_val:
        return (value - min_val) / (max_val - min_val)
    return 0

# Generate color scales
reds_colors = ["#fff5f0", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15", "#67000d"]
yellow_colors = ["#ffffe0", "#fff7bc", "#fee391", "#fec44f", "#fe9929", "#ec7014", "#cc4c02", "#993404", "#662506"]
green_colors = ["#f7fcf5", "#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476", "#41ab5d", "#238b45", "#006d2c", "#00441b"]

def get_color(value, scale, min_val, max_val):
    if pd.isna(value):
        return "white"
    normalized_value = normalize(value, min_val, max_val)
    index = int(normalized_value * (len(scale) - 1))
    return scale[index]

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("LOB Performance Dashboard", style={"color": "#34495e", "font-family": "Arial, sans-serif", "text-align": "center", "font-weight": "bold", "margin-bottom": "20px"}),
    dash_table.DataTable(
        id='heatmap-table',
        columns=[
            {"name": "LOB", "id": "lob"},
            {"name": "Total Seals", "id": "total_seals", "type": "numeric", "format": Format(group=True)},
            {"name": "Red", "id": "Red", "type": "numeric", "format": Format(group=True)},
            {"name": "Yellow", "id": "Yellow", "type": "numeric", "format": Format(group=True)},
            {"name": "Green", "id": "Green", "type": "numeric", "format": Format(group=True)},
            {"name": "Red %", "id": "Red %", "type": "numeric", "format": Format(precision=1, scheme=Scheme.percentage)},
            {"name": "Yellow %", "id": "Yellow %", "type": "numeric", "format": Format(precision=1, scheme=Scheme.percentage)},
            {"name": "Green %", "id": "Green %", "type": "numeric", "format": Format(precision=1, scheme=Scheme.percentage)},
        ],
        data=aggr_data.to_dict('records'),
        style_data_conditional=[
            {
                'if': {'filter_query': f'{{lob}} = "{row["lob"]}"', 'column_id': 'Red'},
                'backgroundColor': get_color(row['Red'], reds_colors, aggr_data['Red'].min(), aggr_data['Red'].max()),
                'color': 'black'
            } for i, row in aggr_data.iterrows()
        ] + [
            {
                'if': {'filter_query': f'{{lob}} = "{row["lob"]}"', 'column_id': 'Yellow'},
                'backgroundColor': get_color(row['Yellow'], yellow_colors, aggr_data['Yellow'].min(), aggr_data['Yellow'].max()),
                'color': 'black'
            } for i, row in aggr_data.iterrows()
        ] + [
            {
                'if': {'filter_query': f'{{lob}} = "{row["lob"]}"', 'column_id': 'Green'},
                'backgroundColor': get_color(row['Green'], green_colors, aggr_data['Green'].min(), aggr_data['Green'].max()),
                'color': 'black'
            } for i, row in aggr_data.iterrows()
        ] + [
            {
                'if': {'filter_query': f'{{lob}} = "{row["lob"]}"', 'column_id': 'Red %'},
                'backgroundColor': get_color(row['Red %'], reds_colors, aggr_data['Red %'].min(), aggr_data['Red %'].max()),
                'color': 'black'
            } for i, row in aggr_data.iterrows()
        ] + [
            {
                'if': {'filter_query': f'{{lob}} = "{row["lob"]}"', 'column_id': 'Yellow %'},
                'backgroundColor': get_color(row['Yellow %'], yellow_colors, aggr_data['Yellow %'].min(), aggr_data['Yellow %'].max()),
                'color': 'black'
            } for i, row in aggr_data.iterrows()
        ] + [
            {
                'if': {'filter_query': f'{{lob}} = "{row["lob"]}"', 'column_id': 'Green %'},
                'backgroundColor': get_color(row['Green %'], green_colors, aggr_data['Green %'].min(), aggr_data['Green %'].max()),
                'color': 'black'
            } for i, row in aggr_data.iterrows()
        ],
        style_header={
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
        style_cell={
            'font-family': 'Arial, sans-serif',
            'textAlign': 'center',
            'fontSize': '14px',
            'padding': '10px'
        },
        style_table={
            'overflowX': 'auto',
            'border': '1px solid #ddd',
            'borderRadius': '10px'
        },
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
