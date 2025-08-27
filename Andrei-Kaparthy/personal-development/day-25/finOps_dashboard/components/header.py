from dash import html

header = html.Div(
    className="header",
    children=[
        html.H1("Interactive FinOps Dashboard"),
        html.P("Upload your AWS Cost & Usage Report to get started")
    ]
)