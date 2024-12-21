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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container(
    [
        html.H1("Open Source License & Seal Insights", className="text-center my-4"),
        
        # Filter and Toggle
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
                        labelStyle={"margin-right": "20px"},
                    ),
                    width=6,
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
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="other_licenses_heatmap"),
                    width=12,
                ),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
)

# Callbacks to update visuals based on LOB filter and display mode
@app.callback(
    [
        Output("strong_copyleft_heatmap", "figure"),
        Output("weak_copyleft_heatmap", "figure"),
        Output("other_licenses_heatmap", "figure"),
    ],
    [Input("lob_filter", "value"), Input("display_mode", "value")],
)
def update_heatmaps(selected_lobs, display_mode):
    # Filter data
    filtered_data = data[data["lob"].isin(selected_lobs)]

    # Calculate sum of unique values from total_seals_lob
    unique_seals_per_lob = filtered_data.groupby("lob")["total_seals_lob"].apply(lambda x: np.unique(x).sum())
    total_seals_all = unique_seals_per_lob.sum()  # Overall total seals

    def create_heatmap(data_subset, colorscale, title):
        # Create a pivot table
        pivot = data_subset.pivot_table(
            index="license_family", columns="lob", values="total_seals", aggfunc="sum"
        ).fillna(0)
        pivot.loc["Total Seals"] = unique_seals_per_lob

        # Calculate percentages
        percentages_per_lob = pivot.div(pivot.loc["Total Seals"], axis=1) * 100
        percentages_total = pivot / total_seals_all * 100

        # Generate text for each mode
        text = pivot.values.astype(int).astype(str)  # Default: numbers
        if display_mode == "percentages":
            text[:-1] = percentages_per_lob[:-1].round(1).astype(str) + "%"  # Exclude Total Seals row
        elif display_mode == "percent_total":
            text[:-1] = percentages_total[:-1].round(1).astype(str) + "%"  # Exclude Total Seals row

        # Create heatmap
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
                hovertemplate=(
                    "License Family: %{y}<br>"
                    "LOB: %{x}<br>"
                    "Seal Count: %{z}<br>"
                    "Percentage: %{customdata:.1f}%<extra></extra>"
                ),
                texttemplate="%{text}",  # Use the generated text
            )
        )
        fig.update_layout(
            title=title,
            xaxis=dict(side="top", tickfont=dict(family="Arial", size=12, color="black")),
            yaxis=dict(tickfont=dict(family="Arial", size=12, color="black")),
        )
        return fig

    # Filter datasets for strong, weak, and other licenses
    strong_copyleft_data = filtered_data[filtered_data["strong_copyleft"] == True]
    weak_copyleft_data = filtered_data[filtered_data["weak_copyleft"] == True]
    other_licenses_data = filtered_data[
        (filtered_data["strong_copyleft"] == False) & (filtered_data["weak_copyleft"] == False)
    ]

    # Create heatmaps
    strong_heatmap_fig = create_heatmap(strong_copyleft_data, "Reds", "Strong Copyleft Licenses by LOB and License Family")
    weak_heatmap_fig = create_heatmap(weak_copyleft_data, "YlOrBr", "Weak Copyleft Licenses by LOB and License Family")
    other_heatmap_fig = create_heatmap(other_licenses_data, "Greens", "Other Licenses by LOB and License Family")

    return strong_heatmap_fig, weak_heatmap_fig, other_heatmap_fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
