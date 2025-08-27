import dash_bootstrap_components as dbc
import pandas as pd
from dash import html

def create_kpi_cards(df: pd.DataFrame):
    """
    Generates a row of KPI cards from the dataframe.
    """
    if df is None or df.empty:
        return []

    total_cost = df['Cost'].sum()
    top_service = df.groupby('Service')['Cost'].sum().idxmax()
    num_days = df['UsageStartDate'].nunique()

    kpi_cards = dbc.Row(
        [
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H4("Total Cost", className="card-title"),
                    html.P(f"${total_cost:,.2f}", className="card-text kpi-value"),
                ])
            ), md=4),
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H4("Top Spending Service", className="card-title"),
                    html.P(top_service, className="card-text kpi-value"),
                ])
            ), md=4),
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H4("Analyzed Period", className="card-title"),
                    html.P(f"{num_days} Days", className="card-text kpi-value"),
                ])
            ), md=4),
        ],
        className="mb-4"
    )
    return kpi_cards
