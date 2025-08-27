import base64
import io

from dash import Dash, dcc, html, Input, Output, State, no_update
import pandas as pd

from components.header import header
from components.uploader import uploader
from components.graphs import create_graphs
from components.report import report_container
from modules.data_loader import parse_contents
from modules.analyzer import get_finops_analysis

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    header,
    uploader,
    html.Div(id='output-container')
])

def create_layout(df):
    """Creates the main layout with graphs and the report section."""
    if df is None:
        return html.Div()
    
    graphs = create_graphs(df)
    report = report_container()
    
    return html.Div([
        html.Div(graphs, className='graphs-container'),
        html.Div(report, className='report-container')
    ])

@app.callback(
    Output('output-container', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    """Callback to update the layout when a file is uploaded."""
    if contents:
        df = parse_contents(contents, filename)
        if isinstance(df, pd.DataFrame):
            return create_layout(df)
        else:
            # Return the error message from parse_contents
            return html.Div([html.H5(df)], className='error-message')
    return no_update

@app.callback(
    Output('report-content', 'children'),
    Input('generate-report-button', 'n_clicks'),
    State('upload-data', 'contents'),
    prevent_initial_call=True
)
def generate_report(n_clicks, contents):
    """Callback to generate and display the FinOps report."""
    if n_clicks > 0 and contents:
        # Decode the base64 string
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        csv_string = decoded.decode('utf-8')
        
        analysis = get_finops_analysis(csv_string)
        return dcc.Markdown(analysis)
    return dcc.Markdown("Click the button to generate the report.")

if __name__ == '__main__':
    app.run(debug=True, port=8050)