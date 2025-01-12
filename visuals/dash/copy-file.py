from dash import Dash, dash_table, html, dcc, Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc

# Sample data
data = {
    "Package Name": ["python-Levenshtein"] * 5,
    "Version": ["0.21.1", "0.25.1", "0.24.0", "0.12.2", "0.25.1"],
    "License": ["GPL-3.0", "GPL-3.0", "GPL-2.0", "GPL-2.0", "GPL-2.0"]
}

df = pd.DataFrame(data)

# Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])  # Using a modern Bootstrap theme

app.layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
        ),
        html.Br(),
        dbc.Button("Open Options", id="open-modal", n_clicks=0, color="primary"),
    ]),

    dbc.Modal(
        [
            dbc.ModalHeader(html.H5("Manage Options")),
            dbc.ModalBody(
                dbc.Tabs([
                    # Tab 1: Copy Link
                    dbc.Tab(
                        label="Copy Link",
                        children=[
                            html.Div([
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H6("Generated Link", className="card-title"),
                                        dcc.Textarea(
                                            id="link-display",
                                            value="https://your-generated-link-here.com",
                                            style={"width": "100%", "height": "100px"},
                                        ),
                                        html.Br(),
                                        dbc.Button(
                                            "Copy to Clipboard",
                                            id="copy-link",
                                            color="info",
                                            n_clicks=0,
                                            className="mt-2"
                                        ),
                                        html.Div(id="copy-status", className="mt-2", style={"color": "green"}),
                                    ])
                                )
                            ])
                        ]
                    ),
                    # Tab 2: Downloads
                    dbc.Tab(
                        label="Downloads",
                        children=[
                            html.Div([
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H6("Download Options", className="card-title"),
                                        html.Div([
                                            dbc.Button(
                                                "Download CSV",
                                                id="download-csv",
                                                color="success",
                                                className="me-2"
                                            ),
                                            dbc.Button(
                                                "Download Excel",
                                                id="download-excel",
                                                color="warning"
                                            ),
                                        ], className="d-flex")
                                    ])
                                )
                            ])
                        ]
                    ),
                ])
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0)
            ),
        ],
        id="modal",
        is_open=False,
        centered=True,
        size="lg"  # Makes the modal larger
    )
])

# Callbacks
@app.callback(
    Output("modal", "is_open"),
    [Input("open-modal", "n_clicks"), Input("close-modal", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("link-display", "value"),
    Input("table", "derived_virtual_data"),
    prevent_initial_call=True
)
def generate_link(data):
    # Generate a dummy link based on the table data
    return "https://generated-link-based-on-table-data.com"


app.clientside_callback(
    """
    function(n_clicks, link) {
        if (n_clicks > 0) {
            navigator.clipboard.writeText(link).then(function() {
                console.log("Copied to clipboard");
            });
            return "Link copied to clipboard!";
        }
        return "";
    }
    """,
    Output("copy-status", "children"),
    Input("copy-link", "n_clicks"),
    State("link-display", "value"),
    prevent_initial_call=True
)


if __name__ == '__main__':
    app.run_server(debug=True)
