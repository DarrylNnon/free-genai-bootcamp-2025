from dash import dcc, html

uploader = html.Div(
    className="upload-container",
    children=[
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select your AWS Cost CSV File')
            ]),
            multiple=False
        )
    ]
)