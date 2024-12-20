import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Sample Data
lob = ["CIB", "CCB", "EP", "AWM", "IP", "CT", "CAO", "EPX", "AMDP", "CTO"]
lob_counts = [1631487, 1594766, 771746, 671891, 579484, 571873, 172564, 98176, 91557, 0]
finding_sources = ["Containers", "OSS", "Qualys", "Managed Vulnerability", "Assessments", "Mobile"]
finding_counts = [3886944, 1827232, 928653, 672197, 3186, 54]

# Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout
app.layout = dbc.Container(
    [
        html.H1("Findings Discovery", className="text-center my-4", style={"font-weight": "bold", "font-family": "Arial, sans-serif"}),

        # Filter Panel
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="lob_filter",
                        options=[{"label": lob_name, "value": lob_name} for lob_name in lob],
                        value=lob,
                        multi=True,
                        placeholder="Select LOB(s)",
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
                                html.H4("Fix Now (INC)", className="text-center", style={"color": "white", "font-weight": "bold"}),
                                html.H2("99", className="text-center", style={"color": "white", "font-weight": "bold", "font-size": "2.5rem"}),
                                html.P("3% ↑ | 5 new", className="text-center", style={"color": "white"}),
                            ]
                        ),
                        style={"backgroundColor": "red", "border-radius": "15px", "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.1)"},
                        className="hover-shadow",
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Fix Next (30 Days)", className="text-center", style={"color": "#856404", "font-weight": "bold"}),
                                html.H2("94,284", className="text-center", style={"color": "#856404", "font-weight": "bold", "font-size": "2.5rem"}),
                                html.P("1% ↑ | 1k new", className="text-center", style={"color": "#856404"}),
                            ]
                        ),
                        style={"backgroundColor": "yellow", "border-radius": "15px", "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.1)"},
                        className="hover-shadow",
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Fix Later (90 Days)", className="text-center", style={"color": "white", "font-weight": "bold"}),
                                html.H2("407,679", className="text-center", style={"color": "white", "font-weight": "bold", "font-size": "2.5rem"}),
                                html.P("1% ↑ | 2k new", className="text-center", style={"color": "white"}),
                            ]
                        ),
                        style={"backgroundColor": "green", "border-radius": "15px", "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.1)"},
                        className="hover-shadow",
                    ),
                    width=4,
                ),
            ]
        ),

        html.Br(),

        # Visualizations
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="heatmap",
                        style={"height": "400px"},
                    ),
                    width=6,
                ),
                dbc.Col(
                    dcc.Graph(
                        id="bar_chart",
                        style={"height": "400px"},
                    ),
                    width=6,
                ),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="lob_chart",
                        style={"height": "400px"},
                    ),
                    width=12,
                )
            ]
        ),
    ],
    fluid=True,
)

# Callbacks to Update Visualizations Based on Filters
@app.callback(
    [
        Output("heatmap", "figure"),
        Output("bar_chart", "figure"),
        Output("lob_chart", "figure"),
    ],
    [Input("lob_filter", "value")],
)
def update_dashboard(selected_lob):
    # Filter LOB Data
    filtered_lob = [lob[i] for i in range(len(lob)) if lob[i] in selected_lob]
    filtered_counts = [lob_counts[i] for i in range(len(lob)) if lob[i] in selected_lob]

    # Heatmap (Static Example)
    heatmap_fig = go.Figure(
        data=go.Heatmap(
            z=[[11118, 78676, 213091, 91238, 23607]],
            x=["V5", "V4", "V3", "V2", "V1"],
            y=["Finding States"],
            colorscale="Blues",
        )
    )
    heatmap_fig.update_layout(title="Heatmap of Findings", xaxis_title="Version")

    # Bar Chart for Finding Sources
    bar_chart_fig = go.Figure(
        data=[
            go.Bar(
                x=finding_sources,
                y=finding_counts,
                name="Finding Sources",
                marker_color="blue",
            )
        ]
    )
    bar_chart_fig.update_layout(title="Finding Sources by Count")

    # LOB Chart
    lob_chart_fig = go.Figure(
        data=[
            go.Bar(
                x=filtered_counts,
                y=filtered_lob,
                orientation="h",
                marker_color="green",
            )
        ]
    )
    lob_chart_fig.update_layout(title="Asset Owning LOB by Count", yaxis_title="LOB")

    return heatmap_fig, bar_chart_fig, lob_chart_fig


# Run the App
if __name__ == "__main__":
    app.run_server(debug=True)
