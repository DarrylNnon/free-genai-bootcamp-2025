from dash import dcc
import plotly.express as px

def create_graphs(df):
    """
    Generates a list of graphs from the dataframe.
    """
    # Ensure 'Cost' is numeric
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
    df.dropna(subset=['Cost'], inplace=True)

    # Graph 1: Cost by Service
    cost_by_service = df.groupby('Service')['Cost'].sum().reset_index().sort_values(by='Cost', ascending=False).head(15)
    fig1 = px.bar(cost_by_service, x='Service', y='Cost', title='Top 15 AWS Services by Cost')

    # Graph 2: Cost Over Time
    # Ensure 'UsageStartDate' is a datetime object
    df['UsageStartDate'] = pd.to_datetime(df['UsageStartDate'])
    cost_over_time = df.groupby(df['UsageStartDate'].dt.date)['Cost'].sum().reset_index()
    fig2 = px.line(cost_over_time, x='UsageStartDate', y='Cost', title='AWS Cost Over Time')

    return [
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2)
    ]

# Note: This is a simplified example. A real-world scenario would involve
# more complex data cleaning and more sophisticated visualizations.