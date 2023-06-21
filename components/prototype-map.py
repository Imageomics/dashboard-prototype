import pandas as pd
from dash import Dash, html, dcc
from graphs import make_map

df = pd.read_csv("test_data/Hoyal_Cuthill_GoldStandard_metadata_cleaned.csv")
df["samples_at_locality"] = df.locality.map(df.locality.value_counts()/2)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Distribution of Samples", style = {'textAlign': 'center', 'color': 'MidnightBlue'}),
    
    # Add empty plot for map
    dcc.Graph(figure = make_map(df), 
              id = 'map')
])

if __name__ == '__main__':
    app.run_server(debug=True)
