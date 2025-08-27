from dash import dcc, html

def report_container():
    """
    Creates the container for the GPT report, including the button.
    """
    return html.Div(
        className="report-container-main",
        children=[
            html.H3("🤖 AI-Powered FinOps Analysis"),
            html.Button("Generate Report", id="generate-report-button", className="report-button"),
            html.Div(id="report-content", children=[dcc.Markdown("Click the button to generate the report.")])
        ]
    )