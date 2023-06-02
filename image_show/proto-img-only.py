import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State
import base64

from query import get_species_options

df = pd.read_csv("test_data/Hoyal_Cuthill_GoldStandard_metadata_cleaned.csv")

app = Dash(__name__)

all_species = get_species_options(df)

app.layout = html.Div([ 
    html.Div([
        html.H4("Show me sample images of ...", style = {"color":"MidnightBlue", 'marginBottom' : 10}),
        #select Species/Subspecies to view (defaul to Any)
        # Note: these should be the same type to interact properly, first must not be clearable
        dcc.Dropdown(options = list(all_species.keys()),
                     value = 'Any',
                     id = 'species-show',
                     clearable = False),
        html.Hr(),
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
    html.Img(id = 'image-1')

])

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
    Output('image-1', 'src'),
    Input('display-img', 'n_clicks'),
    #State('species-show', 'value'),
    State('subspecies-show', 'value'),
    State('which-sex', 'value'),
    State('which-view', 'value'),
    State('hybrid?', 'value'),
    prevent_initial_call = True
)

# Retrieve a single image
def get_image(n_clicks, subspecies, view, sex, hybrid):
    filename = get_filename(subspecies, view, sex, hybrid)
    if filename == 0:
        print("No Such Images. Please make another selection.")
        return
    if 'D_lowres' in filename:
        image_directory = '../test_data/Images/dorsal_images/' + filename
    else:
        image_directory = '../test_data/Images/ventral_images/' + filename
    with open(image_directory, 'rb') as f:
        image = f.read()
    src = 'data:image/tiff;base64,' + base64.b64encode(image).decode()
    #img_path = 'data:image/tiff;base64,' + base64.b64encode(image).decode('utf-8')
    return src

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
        df_sub = df.loc[df.Subspecies == subspecies.lower()].copy()
    if len(view) == 1:
        df_sub = df_sub.loc[df_sub.View == view[0]]
    if len(sex) == 1:
        df_sub = df_sub.loc[df_sub.Sex == sex[0]]
    if len(hybrid) == 1:
        df_filtered = df_sub.loc[df_sub.hybrid_stat == hybrid[0]]
    elif len(hybrid) == 2:
        df_filtered = df_sub.loc[df_sub.hybrid_stat == (hybrid[0] or hybrid[1])]
    else:
        df_filtered = df_sub
    if len(df_filtered) > 0:
        df_filtered.sample(1)
        filename = df_filtered.Image_filename.astype('string').values[0]
        return filename
    else:
        return 0


if __name__ == '__main__':
    app.run_server(debug=True)
