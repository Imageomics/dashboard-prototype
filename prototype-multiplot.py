import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

df = pd.read_csv("test_data/Hoyal_Cuthill_GoldStandard_metadata_cleaned.csv")

app = Dash(__name__)

app.layout = html.Div([
     html.H1("Cuthill Data Distribution Statistics", style = {'textAlign': 'center', 'color': 'MidnightBlue'}),

    #Distribution Options
    html.Div([
        html.Div([
            html.H4("Show me the distribution of ...", style = {"color":"MidnightBlue", 'margin-bottom' : 10}),
            # Add dropdown options
            # x-axis (feature) distribution options: 'Subspecies', 'Additional Taxa Information', 'Locality'
            dcc.RadioItems([
                        {'label': 'Subspecies', 'value': 'Subspecies'},
                        {'label': 'Additional Taxa Information', 'value':'addit_taxa_info'}, 
                        {'label': 'Locality', 'value': 'locality'}], 
                        'Subspecies',
                        id = 'x-variable')
            ], style = {'width': '48%', 'display': 'inline-block'}
            ),
            
        html.Div([
            html.H4("Colored by ...", style = {'color': 'MidnightBlue', 'margin-bottom' : 10}),
        #select color-by option: 'View', 'Sex', 'Hybrid Status'
            dcc.RadioItems([
                            {'label':'View', 'value': 'View'},
                            {'label': 'Sex', 'value': 'Sex'},
                            {'label': 'Hybrid Status', 'value':'hybrid_stat'}],
                            'View',
                            id = 'color-by')
            ], style = {'width': '48%', 'display': 'inline-block'}
        ),
        #html.Br(),
        html.H4("Sort distribution ", style = {'color': 'MidnightBlue', 'margin-top' : 10, 'margin-bottom' : 10}),
        dcc.RadioItems([
                        {'label': 'Alphabetical', 'value': 'alpha'},
                        {'label': 'Ascending', 'value': 'sum ascending'},
                        {'label': 'Descending', 'value': 'sum descending'}],
                        'alpha',
                        id = 'sort-by',
                        inline = True),
        ], style = {'width': '48%', 'display': 'inline-block'}
    ),

    #pie chart options
    html.Div([
        html.H4("Show me the Percentage Breakdown of ...", style = {'color': 'MidnightBlue', 'margin-bottom' : 10}),
        dcc.RadioItems([
                        {'label': 'Species', 'value': 'Species'},
                        {'label': 'Subspecies', 'value': 'Subspecies'},
                        {'label':'View', 'value': 'View'},
                        {'label': 'Sex', 'value': 'Sex'},
                        {'label': 'Hybrid Status', 'value':'hybrid_stat'}],
                        'Species',
                        id = 'prct-brkdwn'
                        ),
        html.Br(),
    ], style = {'width': '48%', 'display': 'inline-block'}
    ),

    html.Br(),
    html.Br(),
       
    #Graphs
    html.Div([
        dcc.Graph(id = 'hist-plot')], style = {'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id = 'pie-plot')], style = {'width': '48%', 'display': 'inline-block'})
])

@app.callback(
    #hist output
    Output(component_id='hist-plot', component_property='figure'),
    #input x_var
    Input(component_id='x-variable', component_property='value'),
    #input color_by
    Input(component_id='color-by', component_property='value'),
    #input sort_by
    Input(component_id='sort-by', component_property='value')
)

def make_hist_plot(x_var, color_by, sort_by):
    #generate histogram
    if sort_by == 'alpha':
        fig = px.histogram(df.sort_values(x_var),
                        x = x_var,
                        color = color_by,
                        color_discrete_sequence = px.colors.qualitative.Bold)
    else:
        fig = px.histogram(df,
                        x = x_var,
                        color = color_by,
                        color_discrete_sequence = px.colors.qualitative.Bold).update_xaxes(categoryorder = sort_by)
    
    fig.update_layout(title = {'text': f'Distribution of {x_var} Colored by {color_by}'})

    return fig

@app.callback(
    #pie output
    Output(component_id='pie-plot', component_property='figure'),
    #pie input (var)
    Input(component_id='prct-brkdwn', component_property='value')
)

def make_pie_plot(var):
    #generate pie chart
    if(var == 'Subspecies'):
        pie_fig = px.pie(df,
                 names = var,
                 color_discrete_sequence = px.colors.qualitative.Bold,
                 hover_data = ['Species'])
    else:
        pie_fig = px.pie(df,
                 names = var,
                 color_discrete_sequence = px.colors.qualitative.Bold)
        pie_fig.update_traces(textposition = 'inside', textinfo = 'percent+label')
    
    pie_fig.update_layout(title = {'text': f'Percentage Breakdown of {var}'})

    return pie_fig

if __name__ == '__main__':
    app.run_server(debug=True)