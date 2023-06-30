from dash import Dash, html, dcc, Input, Output, State
from components.query import get_data, get_species_options, get_images
from components.graphs import make_hist_plot, make_map, make_pie_plot
from components.divs import get_hist_div, get_map_div

# Fixed styles and sorting options
H1_STYLE = {'textAlign': 'center', 'color': 'MidnightBlue'}
H4_STYLE = {'color': 'MidnightBlue', 'margin-bottom' : 10}
HALF_DIV_STYLE = {'width': '48%', 'display': 'inline-block'}
QUARTER_DIV_STYLE = {'width': '24%', 'display': 'inline-block'}
SORT_LIST = [{'label': 'Alphabetical', 'value': 'alpha'},
                {'label': 'Ascending', 'value': 'sum ascending'},
                {'label': 'Descending', 'value': 'sum descending'}]

# get dataset-determined static data:
    # the dataframe and categorical features
    # all possible species, subspecies
    # distribution options (histogram and map options)
df, cat_list = get_data()
all_species = get_species_options(df)
hist_div = get_hist_div(cat_list, SORT_LIST, H4_STYLE, HALF_DIV_STYLE)
map_div = get_map_div(cat_list, H4_STYLE, HALF_DIV_STYLE)

# Initialize app/dashboard and set layout
app = Dash(__name__)

app.layout = html.Div([
     html.H1("Cuthill Data Distribution Statistics", style = H1_STYLE),

    # Distribution Options, default start on histogram
    html.Div(hist_div,
            id = 'dist-options',
            style = HALF_DIV_STYLE
    ),

    # Pie chart options: 'Species', 'Subspecies', 'View', 'Sex', 'Hybrid Status'
    html.Div([
        html.H4("Show me the Percentage Breakdown of ...", style = H4_STYLE),
        dcc.RadioItems(cat_list[:-2],
                        'Species',
                        id = 'prct-brkdwn'
                        ),
        html.Br(),
    ], style = HALF_DIV_STYLE
    ),

    html.Br(),
    html.Br(),
       
    # Graphs - Distribution (histogram or map), then pie chart
    html.Div([
        dcc.Graph(id = 'dist-plot')], style = HALF_DIV_STYLE),
    html.Div([
        dcc.Graph(id = 'pie-plot')], style = HALF_DIV_STYLE),

    html.Hr(),

    html.H1("Cuthill Data Sample Image Selection", style = H1_STYLE),

    html.Hr(),

    # Image Selector
    html.Div([

        html.H4("Show me sample images of ...", style = H4_STYLE),
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
        html.H4("that are ...", style = H4_STYLE),
        html.Div([
            dcc.Checklist(df.Sex.unique(), 
                            df.Sex.unique()[0:2],
                            id = 'which-sex')],
            style = QUARTER_DIV_STYLE
            ),
        html.Div([
            dcc.Checklist(df.View.unique(), 
                            df.View.unique()[0:2],
                            id = 'which-view')],
            style = QUARTER_DIV_STYLE
            ),
        html.Div([
            dcc.Checklist(df.hybrid_stat.unique(), 
                            df.hybrid_stat.unique()[0:2],
                            id = 'hybrid?')],
            style = QUARTER_DIV_STYLE
            ),
        html.Div([
            html.H5("How many images?", style = H4_STYLE),
            dcc.Input(type = 'number',
                        min = 1,
                        max = 100,
                        step = 1,
                        placeholder = '#',
                        id = 'num-images')],
            style = QUARTER_DIV_STYLE
            )
    ], id = 'dropdown-images'),

    html.Hr(),

    # Button to activate the callback
    html.Button('Display Images',
                id = 'display-img',
                n_clicks = 0),

    # Add some space after the button
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

# Distribution Section
# Callback to update which options are visible (histogram vs map)
@app.callback(
        Output('dist-options', 'children'),
        Input('dist-view-btn', 'n_clicks'),
        Input('dist-view-btn', 'children')
)

def update_dist_view(n_clicks, children):
    '''
    Function to update the upper left distribution options based on selected distribution chart (histogram or map).
    Activates on click to change, defaults to histogram view.

    Parameters:
    -----------
    n_clicks - Number of clicks. 
    children - Label on button, determins which distribution options to show.

    Returns:
    --------
    hist_div or map_div - The HTML Div corresponding to the selected distribution figure.
    '''
    if n_clicks == 0:
        return hist_div
    if n_clicks > 0:
        if children == "Show Histogram":
            return hist_div
        else:
            return map_div

# Callback to update the distribution figure (histogram or map)
@app.callback(
    #dist output
    Output(component_id='dist-plot', component_property='figure'),
    #input x_var
    Input(component_id='x-variable', component_property='value'),
    #input color_by
    Input(component_id='color-by', component_property='value'),
    #input sort_by
    Input(component_id='sort-by', component_property='value'),
    #button information
    Input(component_id='dist-view-btn', component_property='children')
)

def update_dist_plot(x_var, color_by, sort_by, btn):
    '''
    Function to update distribution figure with either map or histogram based on selections.
    Selection is based on current label of the button ('Map View' or 'Show Histogram'), which updates prior to graph.

    Parameters:
    -----------
    x_var - User-selected variable to plot distribution.
    color_by - User-selected property to color the plot by.
    sort_by - User-selected ordering of bar charts (Alphabetical, Ascending, or Descending).
    btn - Current label of the button ('Map View' or 'Show Histogram').

    Returns: 
    --------
    fig -  Figure returned from appropriate function call: histogram or map of the distribution of the requested variable.
    '''
    if btn == "Show Histogram":
        return make_map(df, color_by)
    else:
        return make_hist_plot(df, x_var, color_by, sort_by)

# Pie Section

@app.callback(
    #pie output
    Output(component_id='pie-plot', component_property='figure'),
    #pie input (var)
    Input(component_id='prct-brkdwn', component_property='value')
)

def update_pie_plot(var):
    '''
    Updates the pie chart of dataset specimens based on user selection of variable to color by.

    Parameters:
    -----------
    var - User-selected categorical variable by which to color.

    Returns: 
    --------
    fig - Pie chart figure returned from function call: percentage breakdown of `var` samples in the dataset.
    '''
    return make_pie_plot(df, var)

# Image Section

# Callback for Image Species Selection
@app.callback(
    Output(component_id = 'subspecies-show', component_property= 'options'),
    Input(component_id = 'species-show', component_property = 'value')
)

def set_subspecies_options(selected_species):
    # Set subspecies options in dropdown based on user-selected species.
    return [{'label': i, 'value': i} for i in all_species[selected_species]]

# Callback for Image Subspecies Selection
@app.callback(
    Output(component_id = 'subspecies-show', component_property= 'value'),
    Input(component_id = 'subspecies-show', component_property = 'options')
)

def set_subspecies_value(available_options):
    # Collect selected subspecies to display in multi-select dropdown.
    return available_options[0]['value']

# Image & Display Images Button Callback
@app.callback(
    Output('image-1', 'children'),
    Input('display-img', 'n_clicks'),
    #State('species-show', 'value'),
    State('subspecies-show', 'value'),
    State('which-view', 'value'),
    State('which-sex', 'value'),
    State('hybrid?', 'value'),
    State('num-images', 'value'),
    prevent_initial_call = True
)

# Retrieve selected number of images
def update_display(n_clicks, subspecies, view, sex, hybrid, num_images):
    '''
    Function to retrieve the user-selected number of images adhering to their chosen parameters when the 'Display Images' button is pressed.
    
    Parameters:
    -----------
    n_clicks - Number of times the 'Display Images' button has been pressed.
    subspecies - String. Subspecies of specimen selected by the user.
    view - String. View of specimen selected by the user.
    sex - String. Sex of specimen selected by the user.
    hybrid - String. Hybrid status of specimen selected by the user.
    num_images - Integer. Number of images requested by the user. Default value is 1 (in get_filename).
    
    Returns:
    --------
    Imgs - (Return of function call) List of html image elements with `src` element pointing to paths for the requested number of images matching given parameters.
           Returns html header4 "No Such Images. Please make another selection." if no images matching parameters exist.
           Returns html header4 "Please make a selection." If number of images isn't specified.
    '''
    if n_clicks > 0 and (view != [] and sex != [] and hybrid != []):
        return get_images(df, subspecies, view, sex, hybrid, num_images)
    else:
        return html.H4("Please make a selection.", 
                    style = {'color': 'MidnightBlue'})

if __name__ == '__main__':
    app.run_server(debug=True)
