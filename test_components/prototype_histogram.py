import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

df = pd.read_csv("test_data/Hoyal_Cuthill_GoldStandard_metadata_cleaned.csv")

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Choose your distribution", style = {"color":"blue", "justify-content": "center"}),
    # Add dropdown options
    # x-axis (feature) distribution options: 'Subspecies', 'Additional Taxa Information', 'Locality'
    dcc.Dropdown(['Subspecies', 'addit_taxa_info', 'locality'],
                 'Subspecies',
                 id = 'x-variable'),
    html.Br(),
    #html.Div(id='dd1-output'),
    #select color-by option: 'View', 'Sex', 'Hybrid Status'
    dcc.RadioItems(['View', 'Sex', 'hybrid_stat'],
                 'View',
                 id = 'color-by'),
    html.Br(),
    #html.Div(id = 'dd2-output'),
    # Add empty plot for histogram
    dcc.Graph(id = 'plot')
])

@app.callback(
    # output
    Output(component_id='plot', component_property='figure'),
    #input1
    Input(component_id='x-variable', component_property='value'),
    #input2
    Input(component_id='color-by', component_property='value')
)

def make_plot(x_var, color_by):
    fig = px.histogram(df.sort_values(x_var),
                       x = x_var,
                       color = color_by)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)