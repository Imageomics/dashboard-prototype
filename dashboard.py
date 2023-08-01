import pandas as pd
import base64
import io
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import DashProxy, Serverside, ServersideOutputTransform, html, dcc, Input, Output, State
from components.query import get_data, get_species_options, get_images
from components.graphs import make_hist_plot, make_map, make_pie_plot
from components.divs import get_main_div, get_error_div, get_hist_div, get_map_div, get_img_div

# Fixed style
PRINT_STYLE = {'textAlign': 'center', 'color': 'MidnightBlue', 'margin-bottom' : 10}

# Initialize app/dashboard and set layout
app = DashProxy(__name__, 
                suppress_callback_exceptions = True, 
                transforms = [ServersideOutputTransform()])

app.layout = html.Div([
                dcc.Upload(html.Button('Upload Data',
                                    style = {'color': 'MidnightBlue', 
                                            'background-color': 'BlanchedAlmond', 
                                            'border-color': 'MidnightBlue',
                                            'font-size': '16px'}),
                            id = 'upload-data',
                            multiple = False
                            ),
                # Set up memory store, will revert on page refresh
                dcc.Store(id = 'memory'),
                html.Hr(),
                
                html.Div(children = [html.H3('Upload data (CSV or XLS) to see distribution statistics.', 
                                              style = PRINT_STYLE),
                                    html.Br(),
                                    html.P(["For further file requirements, please see the ",
                                            html.A("documentation",
                                                    href="https://github.com/Imageomics/dashboard-prototype#how-it-works",
                                                    target='_blank'),
                                                    "."],
                                              style = PRINT_STYLE)],
                         id = 'output-data-upload')
])

# Data read in and saved to memory
@app.callback(
        Output('memory', 'data', allow_duplicate=True),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call = True
)

def parse_contents(contents, filename):
    '''
    Function to read uploaded data. Saves processed data to server for faster callbacks.
    Returns dictionary of processed data and divs or the appropriate error message.
    '''
    if contents is None:
        raise PreventUpdate
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return {'error': {'type': 'wrong file type'}}
    except UnicodeDecodeError as e:
        print(e)
        return {'error': {'unicode': str(e)}}
    
    except Exception as e:
        print(e)
        return {'error': {'other': str(e)}}
    # Check for required columns
    # If no lat/lon, disable Map View button
    # If no image urls, disable sample image options
    mapping = True
    img_urls = True
    features = ['Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lat', 'lon', 'file_url', 'Image_filename']
    included_features = []
    for feature in features:
        if feature not in list(df.columns):
            if feature == 'lat' or feature == 'lon':
                mapping = False
            elif feature == 'file_url':
                img_urls = False
            elif feature == 'Image_filename':
                # If 'Image_filename' missing, return missing column if 'file_url' is included.
                if img_urls:
                    return {'error': {'feature': feature}}
            else:
                return {'error': {'feature': feature}}
        else:
            included_features.append(feature)
    
    # get dataset-determined static data:
        # the dataframe and categorical features - processed for map view if mapping is True
        # all possible species, subspecies
        # will likely include categorical options in later instance (sooner)
    processed_df, cat_list = get_data(df, mapping, included_features)
    all_species = get_species_options(processed_df)

    # Use the processed data to get the main div (components: histogram, pie chart, and image example options).
    hist_div = get_hist_div(mapping)
    img_div = get_img_div(processed_df, all_species, img_urls)
    main_div = get_main_div(hist_div, img_div)
    
    # save data to dictionary to save on server
    data = {
            'processed_df': processed_df,
            'all_species': all_species,
            # 'cats': cat_list
            'hist': hist_div,
            'main': main_div
        }   
    
    if mapping:
        data['mapping'] = get_map_div()

    return Serverside(data)

# Callback to update processed data if new data uploaded
@app.callback(
        Output('memory', 'data'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call = True
)
    
def update_output(contents, filename):
    if contents is not None:
        return parse_contents(contents, filename)

# Callback to display main div (histogram, pie chart, and image example options).
@app.callback(
        Output('output-data-upload', 'children'),
        Input('memory', 'data'),
        prevent_initial_call = True
)

def get_visuals(data):
    '''
    Function that returns the main div (histogram, pie chart, and image example options).
    Returns error div if error occurs in upload or essential features are missing.
    '''
    if 'error' in data:
        return get_error_div(data['error'])
    
    return data['main']

# Distribution Section
# Callback to update which options are visible (histogram vs map).
@app.callback(
        Output('dist-options', 'children'),
        Input('dist-view-btn', 'n_clicks'),
        Input('dist-view-btn', 'children'),
        Input('memory', 'data')
)

def update_dist_view(n_clicks, children, data):
    '''
    Function to update the upper left distribution options based on selected distribution chart (histogram or map).
    Activates on click to change, defaults to histogram view.

    Parameters:
    -----------
    n_clicks - Number of clicks. 
    children - Label on button, determins which distribution options to show.
    data - Saved dictionary of DataFrame, species options, and divs (hist and main).

    Returns:
    --------
    data['hist'] or data['mapping'] - The HTML Div corresponding to the selected distribution figure (histogram or map, respectively).
    '''
    if n_clicks == 0 or n_clicks == None:
        return data['hist']
    if n_clicks > 0:
        if children == "Show Histogram":
            return data['hist']
        else:
            return data['mapping']

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
    Input(component_id='dist-view-btn', component_property='children'),
    # Saved Data
    Input('memory', 'data')
)

def update_dist_plot(x_var, color_by, sort_by, btn, data):
    '''
    Function to update distribution figure with either map or histogram based on selections.
    Selection is based on current label of the button ('Map View' or 'Show Histogram'), which updates prior to graph.

    Parameters:
    -----------
    x_var - User-selected variable to plot distribution.
    color_by - User-selected property to color the plot by.
    sort_by - User-selected ordering of bar charts (Alphabetical, Ascending, or Descending).
    btn - Current label of the button ('Map View' or 'Show Histogram').
    data - Saved dictionary of DataFrame, species options, and divs (hist and main).

    Returns: 
    --------
    fig -  Figure returned from appropriate function call: histogram or map of the distribution of the requested variable.
    '''
    # get distribution graph based on button value
    if btn == "Show Histogram":
        return make_map(data['processed_df'], color_by)
    else:
        return make_hist_plot(data['processed_df'], x_var, color_by, sort_by)

# Pie Section

@app.callback(
    #pie output
    Output(component_id='pie-plot', component_property='figure'),
    #pie input (var)
    Input(component_id='prct-brkdwn', component_property='value'),
    # Saved Data
    Input('memory', 'data')
)

def update_pie_plot(var, data):
    '''
    Updates the pie chart of dataset specimens based on user selection of variable to color by.

    Parameters:
    -----------
    var - User-selected categorical variable by which to color.
    data - Saved dictionary of DataFrame, species options, and divs (hist and main).

    Returns: 
    --------
    fig - Pie chart figure returned from function call: percentage breakdown of `var` samples in the dataset.
    '''
    return make_pie_plot(data['processed_df'], var)

# Image Section

# Callback for Image Species Selection
@app.callback(
    Output(component_id = 'subspecies-show', component_property= 'options'),
    Input(component_id = 'species-show', component_property = 'value'),
    Input('memory', 'data')
)

def set_subspecies_options(selected_species, data):
    ''' 
    Function to set subspecies options in dropdown based on user-selected species.

    Parameters:
    -----------
    data - Saved dictionary of DataFrame, species options, and divs (hist and main).

    Returns: 
    --------
    list of subspecies options based on user-selected species. 
    '''
    all_species = data['all_species']
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
    Input('memory', 'data'),
    State('subspecies-show', 'value'),
    State('which-view', 'value'),
    State('which-sex', 'value'),
    State('hybrid?', 'value'),
    State('num-images', 'value'),
    prevent_initial_call = True
)

# Retrieve selected number of images
def update_display(n_clicks, data, subspecies, view, sex, hybrid, num_images):
    '''
    Function to retrieve the user-selected number of images adhering to their chosen parameters when the 'Display Images' button is pressed.
    
    Parameters:
    -----------
    n_clicks - Number of times the 'Display Images' button has been pressed.
    data - Saved dictionary of DataFrame, species options, and divs (hist and main).
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
        return get_images(data['processed_df'], subspecies, view, sex, hybrid, num_images)
    else:
        return html.H4("Please make a selection.", 
                    style = {'color': 'MidnightBlue'})

if __name__ == '__main__':
    app.run_server(debug=True)
