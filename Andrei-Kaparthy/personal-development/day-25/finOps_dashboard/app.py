import base64
import io

from dash import Dash, dcc, html, Input, Output, State, no_update, clientside_callback, ClientsideFunction
import dash_bootstrap_components as dbc
import pandas as pd

from components.header import header
from components.uploader import uploader
from components.graphs import create_graphs
from components.report import report_container
from components.kpi import create_kpi_cards
from modules.data_loader import parse_contents
from modules.analyzer import get_finops_analysis

# Initialize the Dash app
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    external_scripts=[
        {"src": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"}
    ],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

app.layout = html.Div([
    dcc.Store(id='df-store'),
    header,
    dbc.Container(
        [
            uploader,
            html.Div(id='output-container')
        ],
        fluid=True
    )
])

@app.callback(
    [Output('output-container', 'children'),
     Output('df-store', 'data')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    """Callback to update the layout when a file is uploaded."""
    if contents:
        df_or_error = parse_contents(contents, filename)
        if not isinstance(df_or_error, pd.DataFrame):
            # Return the error message from parse_contents
            error_layout = dbc.Alert(df_or_error, color="danger", className="mt-4")
            return error_layout, no_update

        df = df_or_error
        # Create the main layout with graphs and the report section
        kpis = create_kpi_cards(df)
        graphs = create_graphs(df)
        report = report_container()

        layout = html.Div([
            kpis,
            dbc.Card(dbc.CardBody(graphs)),
            report
        ])

        # Store dataframe as JSON in dcc.Store
        return layout, df.to_json(date_format='iso', orient='split')

    return no_update, no_update

@app.callback(
    Output('report-content', 'children'),
    Input('generate-report-button', 'n_clicks'),
    State('df-store', 'data'),
    prevent_initial_call=True
)
def generate_report(n_clicks, json_data):
    """Callback to generate and display the FinOps report."""
    if n_clicks > 0 and json_data:
        df = pd.read_json(json_data, orient='split')
        csv_string = df.to_csv(index=False)
        analysis = get_finops_analysis(csv_string)
        return dcc.Markdown(analysis)
    return ""

# Clientside callback to switch themes
clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='switch_theme'),
    Output('theme-switch', 'id'), # Dummy output
    Input('theme-switch', 'value'),
)

if __name__ == '__main__':
    app.run(debug=True, port=8050)