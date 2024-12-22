import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Load data
file_path = 'data.csv'
data = pd.read_csv(file_path)

# Start Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Sidebar
def create_sidebar():
    return dbc.Container(
        [
            html.Div(
                "OSG",
                className="osa-header",  # Apply the modern styling
            ),
            html.Hr(style={"border-top": "1px solid #dee2e6"}),  # Subtle border
            dbc.Nav(
                [
                    dbc.NavItem(html.Div("Consumption", className="nav-category")),
                    dbc.NavLink("License & Seal Insights", href="/license_insights", id="nav-link-license-insights", className="modern-navlink"),
                    dbc.NavLink("License Coverage", href="/dashboard2", id="nav-link-dashboard2", className="modern-navlink"),
                    dbc.NavItem(html.Div("Contribution", className="nav-category")),
                    dbc.NavLink("Executive Dashboard", href="/dashboard5", id="nav-link-dashboard5", className="modern-navlink"),
                    dbc.NavLink("Analytics", href="/dashboard6", id="nav-link-dashboard6", className="modern-navlink"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        className="dash-container",
    )


# Layout for Dashboard 1
def create_dashboard1():
    return dbc.Container(
        [
            html.H1(
                "Open Source License & Seal Insights",
                className="dashboard-title",  # Apply modern styling
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            id="lob_filter",
                            options=[{"label": lob, "value": lob} for lob in data["lob"].unique()],
                            value=data["lob"].unique().tolist(),
                            multi=True,
                            placeholder="Filter by Line of Business (LOB)",
                            style={"border-radius": "5px", "padding": "10px"},
                        ),
                        width=7,
                    ),
                    dbc.Col(
                        dcc.RadioItems(
                            id="display_mode",
                            options=[
                                {"label": "Seal Counts", "value": "numbers"},
                                {"label": "Seal Percentage (LOB)", "value": "percentages"},
                                {"label": "Seal Percentage (Overall)", "value": "percent_total"},
                            ],
                            value="percent_total",
                            inline=True,
                            labelStyle={"margin-right": "15px"},
                            # className="radio-buttons",  # Apply modern styling
                        ),
                         width=2,  # Centered radio buttons
                    ),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Strong Copyleft Licenses", style={"font-size": "1.2rem", "font-weight": "600", "color": "#495057"}),
                                dbc.CardBody(dcc.Graph(id="strong_copyleft_heatmap")),
                            ],
                            className="mb-4",
                            style={"box-shadow": "0 4px 8px rgba(0,0,0,0.1)", "border-radius": "8px"},
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Weak Copyleft Licenses", style={"font-size": "1.2rem", "font-weight": "600", "color": "#495057"}),
                                dbc.CardBody(dcc.Graph(id="weak_copyleft_heatmap")),
                            ],
                            className="mb-4",
                            style={"box-shadow": "0 4px 8px rgba(0,0,0,0.1)", "border-radius": "8px"},
                        ),
                        width=6,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Other Licenses", style={"font-size": "1.2rem", "font-weight": "600", "color": "#495057"}),
                                dbc.CardBody(dcc.Graph(id="other_licenses_heatmap")),
                            ],
                            className="mb-4",
                            style={"box-shadow": "0 4px 8px rgba(0,0,0,0.1)", "border-radius": "8px"},
                        ),
                        width=12,
                    ),
                ]
            ),
        ],
        style={"margin-left": "220px", "padding": "20px", "background-color": "#f8f9fa", "width": "calc((100% - 220px))"},
        fluid=True,
    )


# , "width": "calc((100% - 220px))"
# Layout for Dashboard 2
def create_dashboard2():
    return dbc.Container(
        [
            html.H1("Dashboard 2: License Coverage", className="text-center my-4"),
            html.P("This is where the content for Dashboard 2 will go."),
        ],
        style={"margin-left": "220px", "padding": "20px"},
        fluid=True,
    )

# Placeholder Dashboard
def create_placeholder_dashboard():
    return dbc.Container(
        [
            html.H1("Placeholder Dashboard", className="text-center my-4"),
            html.P("This is where content for additional dashboards will go."),
        ],
        style={"margin-left": "220px", "padding": "20px"},
        fluid=True,
    )

# Main Layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        create_sidebar(),
        html.Div(id="page-content"),
    ]
)

# Callbacks for Navigation
@app.callback(
    [Output("page-content", "children")] +
    [Output(f"nav-link-{page}", "active") for page in ["license-insights", "dashboard2", "dashboard5", "dashboard6"]],
    [Input("url", "pathname")]
)
def display_page_and_highlight(pathname):
    # Default to License & Seal Insights
    if pathname in ["/", "/license_insights"]:
        return (
            create_dashboard1(),
            True,  # Highlight License Insights
            False, False, False,  # Other links inactive
        )
    elif pathname == "/dashboard2":
        return (
            create_dashboard2(),
            False,
            True,  # Highlight License Coverage
            False, False,
        )
    elif pathname == "/dashboard5":
        return (
            create_placeholder_dashboard(),
            False,
            False,
            True,  # Highlight Executive Dashboard
            False,
        )
    elif pathname == "/dashboard6":
        return (
            create_placeholder_dashboard(),
            False,
            False,
            False,
            True,  # Highlight Analytics
        )
    else:
        return (
            create_placeholder_dashboard(),
            False, False, False, False,  # All links inactive
        )

# Heatmap Creation Function
def create_heatmap(data_subset, colorscale, title, display_mode, unique_seals_per_lob, total_seals_all):
    pivot = data_subset.pivot_table(
        index="license_family", columns="lob", values="total_seals", aggfunc="sum"
    ).fillna(0)
    pivot.loc["Total Seals"] = unique_seals_per_lob

    percentages_per_lob = pivot.div(pivot.loc["Total Seals"], axis=1) * 100
    percentages_total = pivot / total_seals_all * 100

    text = pivot.values.astype(int).astype(str)
    if display_mode == "percentages":
        text[:-1] = percentages_per_lob[:-1].round(1).astype(str) + "%"
    elif display_mode == "percent_total":
        text[:-1] = percentages_total[:-1].round(1).astype(str) + "%"

    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            z=pivot.values,
            customdata=percentages_total.values if display_mode == "percent_total" else percentages_per_lob.values,
            text=text,
            x=pivot.columns,
            y=pivot.index,
            colorscale=colorscale,
            showscale=False,
            hovertemplate="License Family: %{y}<br>LOB: %{x}<br>Seal Count: %{z}<br>Percentage: %{customdata:.1f}%<extra></extra>",
            texttemplate="%{text}",
        )
    )
    fig.update_layout(
        title=None,  # Remove title
        margin=dict(t=20, b=20, l=20, r=20),  # Reduce top, bottom, left, right margins
        height=270,  # Set the height of the chart (in pixels)
        xaxis=dict(
            title="",  # Remove x-axis title
            side="top",  # Position x-axis labels on top
            tickfont=dict(
                family="Arial, sans-serif",  # Modern font
                size=12,  # Font size
                color="#343a40",  # Dark gray for modern look
                weight="bold",  # Make labels bold
            ),
            automargin=True,  # Allow space for tick labels
        ),
        yaxis=dict(
            title="",  # Remove y-axis title
            tickfont=dict(
                family="Arial, sans-serif",  # Modern font
                size=12,  # Font size
                color="#343a40",  # Dark gray for modern look
                weight="bold",  # Make labels bold
            ),
            automargin=True,  # Allow space for y-axis labels
        ),
    )
    return fig

# Heatmap Callback
@app.callback(
    [
        Output("strong_copyleft_heatmap", "figure"),
        Output("weak_copyleft_heatmap", "figure"),
        Output("other_licenses_heatmap", "figure"),
    ],
    [Input("lob_filter", "value"), Input("display_mode", "value")],
)
def update_heatmaps(selected_lobs, display_mode):
    filtered_data = data[data["lob"].isin(selected_lobs)]
    unique_seals_per_lob = filtered_data.groupby("lob")["total_seals_lob"].apply(lambda x: np.unique(x).sum())
    total_seals_all = unique_seals_per_lob.sum()

    strong_data = filtered_data[filtered_data["strong_copyleft"] == True]
    weak_data = filtered_data[filtered_data["weak_copyleft"] == True]
    other_data = filtered_data[(filtered_data["strong_copyleft"] == False) & (filtered_data["weak_copyleft"] == False)]

    strong_heatmap = create_heatmap(strong_data, "Reds", "Strong Copyleft Licenses", display_mode, unique_seals_per_lob, total_seals_all)
    weak_heatmap = create_heatmap(weak_data, "YlOrBr", "Weak Copyleft Licenses", display_mode, unique_seals_per_lob, total_seals_all)
    other_heatmap = create_heatmap(other_data, "Greens", "Other Licenses", display_mode, unique_seals_per_lob, total_seals_all)

    return strong_heatmap, weak_heatmap, other_heatmap

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
