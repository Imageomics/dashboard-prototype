import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State
from test_components.query import get_species_options

df = pd.read_csv("test_data/Hoyal_Cuthill_GoldStandard_metadata_cleaned.csv")
all_species = get_species_options(df)

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
        dcc.Graph(id = 'pie-plot')], style = {'width': '48%', 'display': 'inline-block'}),

    html.Hr(),

    html.H1("Cuthill Data Sample Image Selection", style = {'textAlign': 'center', 'color': 'MidnightBlue'}),

    html.Hr(),

    # Image Selector
    html.Div([

        html.H4("Show me sample images of ...", style = {"color":"MidnightBlue", 'marginBottom' : 10}),
        #select Species/Subspecies to view (defaul to Any)
        # Note: these should be the same type to interact properly, first must not be clearable
        dcc.Dropdown(options = list(all_species.keys()),
                        value = 'Any',
                        id = 'species-show',
                        clearable = False),
        #html.Br(),
        dcc.Dropdown(
                        multi = True,
                        id = 'subspecies-show',
                        placeholder = 'Select Subspecies to View'),
        # Further Refine by Features
        html.H4("that are ...", style = {"color":"MidnightBlue", 'marginBottom' : 10}),
        html.Div([
            dcc.Checklist(df.Sex.unique(), 
                            df.Sex.unique()[0:2],
                            id = 'which-sex')],
            style = {'width': '24%', 'display': 'inline-block'}
            ),
        html.Div([
            dcc.Checklist(df.View.unique(), 
                            df.View.unique()[0:2],
                            id = 'which-view')],
            style = {'width': '24%', 'display': 'inline-block'}
            ),
        html.Div([
            dcc.Checklist(df.hybrid_stat.unique(), 
                            df.hybrid_stat.unique()[0:2],
                            id = 'hybrid?')],
            style = {'width': '24%', 'display': 'inline-block'}
            )
    ], id = 'dropdown-images'),

    html.Hr(),

    #Button to activate the callback
    html.Button('Display Images',
                id = 'display-img',
                n_clicks = 0),

    # Add some space after the button
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    # Image Should appear
    html.Div(id = 'image-1'),

    # Add some space after the image to push up
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

])

# Histogram Section

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

# Pie Section

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

# Image Section

# Callback for Image Species Selection
@app.callback(
    Output(component_id = 'subspecies-show', component_property= 'options'),
    Input(component_id = 'species-show', component_property = 'value')
)

def set_subspecies_options(selected_species):
    # Set subspecies options based on selected species
    return [{'label': i, 'value': i} for i in all_species[selected_species]]

# Callback for Image Subspecies Selection
@app.callback(
    Output(component_id = 'subspecies-show', component_property= 'value'),
    Input(component_id = 'subspecies-show', component_property = 'options')
)

def set_subspecies_value(available_options):
    # Collect selected subspecies
    return available_options[0]['value']

@app.callback(
    Output('image-1', 'children'),
    Input('display-img', 'n_clicks'),
    #State('species-show', 'value'),
    State('subspecies-show', 'value'),
    State('which-view', 'value'),
    State('which-sex', 'value'),
    State('hybrid?', 'value'),
    prevent_initial_call = True
)

# Retrieve a single image
def get_image(n_clicks, subspecies, view, sex, hybrid):
    #if n_clicks is None:
    #    raise PreventUpdate
   # else:
    filename = get_filename(subspecies, view, sex, hybrid)
    if filename == 0:
        #print("No Such Images. Please make another selection.")
        return html.H4("No Such Images. Please make another selection.", 
                    style = {"color":"MidnightBlue"})
    if 'D_lowres' in filename:    
        image_directory = "dorsal_images/"
    else:
        image_directory = "ventral_images/"
    #remove 'tif' from filename and replace with 'png' in url
    image_path = "https://github.com/Imageomics/dashboard-prototype/blob/feature/image-options/test_data/images/" + image_directory + filename[:-3] + "png?raw=true"
    return html.Img(src = image_path)

def get_filename(subspecies, view, sex, hybrid):
    #filter df by subspecies, then view, sex and hybrid
    #return filenames for 7 randomly selected images from the filtered dataset
    #check for Any-Melpomene, Any-Erato, or Any (general)
    if 'Any' in subspecies:
        if subspecies == 'Any':
            df_sub = df.copy()
        else:
            subspecies = subspecies.split('-')[1].lower()
            df_sub = df.loc[df.Subspecies == subspecies].copy()
    else:
         df_sub = df.loc[df.Subspecies.isin(subspecies)].copy()
    df_sub = df_sub.loc[df_sub.View.isin(view)]
    df_sub = df_sub.loc[df_sub.Sex.isin(sex)]
    df_filtered = df_sub.loc[df_sub.hybrid_stat.isin(hybrid)]
    if len(df_filtered) > 0:
        df_filtered.sample(1)
        filename = df_filtered.Image_filename.astype('string').values[0]
        return filename
    else:
        return 0

if __name__ == '__main__':
    app.run_server(debug=True)