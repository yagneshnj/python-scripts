import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Sample Data
lob = ["CIB", "CCB", "EP", "AWM", "IP", "CT", "CAO", "EPX", "AMDP", "CTO"]
lob_counts = [1631487, 1594766, 771746, 671891, 579484, 571873, 172564, 98176, 91557, 0]

# Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout
app.layout = dbc.Container(
    [
        html.H1("Findings Discovery", className="text-center my-3"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Fix Now (INC)", className="text-center text-danger"),
                            html.H2("99", className="text-center text-danger"),
                            html.P("3% ↑ | 5 new", className="text-center"),
                        ]
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Fix Next (30 Days)", className="text-center text-warning"),
                            html.H2("94,284", className="text-center text-warning"),
                            html.P("1% ↑ | 1k new", className="text-center"),
                        ]
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Fix Later (90 Days)", className="text-center text-primary"),
                            html.H2("407,679", className="text-center text-primary"),
                            html.P("1% ↑ | 2k new", className="text-center"),
                        ]
                    ),
                    width=4,
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="heatmap",
                        figure=go.Figure(
                            data=go.Heatmap(
                                z=[[11118, 78676, 213091, 91238, 23607]],
                                x=["V5", "V4", "V3", "V2", "V1"],
                                y=["Finding States"],
                                colorscale="Blues",
                            )
                        ).update_layout(title="Heatmap of Findings", xaxis_title="Version"),
                    ),
                    width=6,
                ),
                dbc.Col(
                    dcc.Graph(
                        id="bar_chart",
                        figure=go.Figure(
                            data=[
                                go.Bar(
                                    x=["Containers", "OSS", "Qualys", "Managed Vulnerability", "Assessments", "Mobile"],
                                    y=[3886944, 1827232, 928653, 672197, 3186, 54],
                                    name="Finding Sources",
                                    marker_color="blue",
                                )
                            ]
                        ).update_layout(title="Finding Sources by Count"),
                    ),
                    width=6,
                ),
            ]
        ),
        html.Br(),
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
                    width=4,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="lob_chart"),
                    width=12,
                )
            ]
        ),
    ],
    fluid=True,
)

# Callback to Update LOB Chart Based on Filter
@app.callback(
    Output("lob_chart", "figure"),
    Input("lob_filter", "value"),
)
def update_lob_chart(selected_lob):
    if not selected_lob:
        filtered_lob = []
        filtered_counts = []
    else:
        filtered_lob = [lob[i] for i in range(len(lob)) if lob[i] in selected_lob]
        filtered_counts = [lob_counts[i] for i in range(len(lob)) if lob[i] in selected_lob]

    fig = go.Figure(
        data=[
            go.Bar(
                x=filtered_counts,
                y=filtered_lob,
                orientation="h",
                marker_color="green",
            )
        ]
    )
    fig.update_layout(title="Asset Owning LOB by Count", yaxis_title="LOB")
    return fig


# Run the App
if __name__ == "__main__":
    app.run_server(debug=True)
