import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load data
file_path = 'data.csv'
data = pd.read_csv(file_path)

# Calculate distinct total_seals_lob sum
total_seals_lob_sum = data['total_seals_lob'].nunique()

# Start Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container(
    [
        html.H1("License Analytics Dashboard", className="text-center my-4"),
        
        # Filter
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="lob_filter",
                        options=[{"label": lob, "value": lob} for lob in data["lob"].unique()],
                        value=data["lob"].unique().tolist(),
                        multi=True,
                        placeholder="Filter by LOB",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        # Metrics Cards
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Total Seals", className="text-center", style={"color": "white"}),
                                html.H2(f"{total_seals_lob_sum}", className="text-center", style={"color": "white"}),
                            ]
                        ),
                        style={"backgroundColor": "green", "border-radius": "15px", "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.1)"},
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Strong Copyleft Licenses", className="text-center", style={"color": "white"}),
                                html.H2(f"{data['strong_copyleft'].sum()}", className="text-center", style={"color": "white"}),
                            ]
                        ),
                        style={"backgroundColor": "red", "border-radius": "15px", "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.1)"},
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Weak Copyleft Licenses", className="text-center", style={"color": "black", "font-weight": "bold"}),
                                html.H2(f"{data['weak_copyleft'].sum()}", className="text-center", style={"color": "black", "font-weight": "bold"}),
                            ]
                        ),
                        style={"backgroundColor": "yellow", "border-radius": "15px", "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.1)"},
                    ),
                    width=4,
                ),
            ],
            className="mb-4",
        ),
        
        # Visualizations
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="strong_copyleft_heatmap"),
                    width=6,
                ),
                dbc.Col(
                    dcc.Graph(id="weak_copyleft_heatmap"),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        # Table-Like View
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="other_licenses_table", style={"width": "100%", "height": "600px"}),
                    width=12,
                )
            ],
        ),
    ],
    fluid=True,
)

# Callbacks to update visuals based on LOB filter
@app.callback(
    [
        Output("strong_copyleft_heatmap", "figure"),
        Output("weak_copyleft_heatmap", "figure"),
        Output("other_licenses_table", "figure"),
    ],
    [Input("lob_filter", "value")],
)
def update_visuals(selected_lobs):
    # Filter data
    filtered_data = data[data["lob"].isin(selected_lobs)]

    # Strong Copyleft Heatmap with Annotations
    strong_heatmap = px.density_heatmap(
        filtered_data[filtered_data["strong_copyleft"] == True],
        x="lob",
        y="license_family",
        z="total_seals",
        color_continuous_scale="Reds",
        title="Strong Copyleft Licenses by LOB and License Family",
    )
    strong_heatmap.update_traces(
        texttemplate="%{z}", textfont_size=10, textfont_color="black"
    )

    # Weak Copyleft Heatmap (Yellow Shades) with Annotations
    weak_heatmap = px.density_heatmap(
        filtered_data[filtered_data["weak_copyleft"] == True],
        x="lob",
        y="license_family",
        z="total_seals",
        color_continuous_scale="YlOrBr",
        title="Weak Copyleft Licenses by LOB and License Family",
    )
    weak_heatmap.update_traces(
        texttemplate="%{z}", textfont_size=10, textfont_color="black"
    )

    # Table for Licenses Without Strong or Weak Copyleft (Green Shades)
    other_licenses = filtered_data[
        (filtered_data["strong_copyleft"] == False) & (filtered_data["weak_copyleft"] == False)
    ]
    other_table_fig = px.imshow(
        other_licenses.pivot_table(
            index="license_family",
            columns="lob",
            values="total_seals",
            aggfunc="sum",
        ),
        color_continuous_scale="Greens",
        title="Other Licenses (No Strong or Weak Copyleft) by LOB",
    )
    other_table_fig.update_traces(
        texttemplate="%{z}", textfont_size=10, textfont_color="black"
    )

    return strong_heatmap, weak_heatmap, other_table_fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
