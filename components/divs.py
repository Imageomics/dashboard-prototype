from dash import html, dcc

# Fixed styles and sorting options
H1_STYLE = {'textAlign': 'center', 'color': 'MidnightBlue'}
H4_STYLE = {'color': 'MidnightBlue', 'margin-bottom' : 10}
HALF_DIV_STYLE = {'height': '48%', 'width': '48%', 'display': 'inline-block'}
QUARTER_DIV_STYLE = {'width': '24%', 'display': 'inline-block'}
BUTTON_STYLE = {'color': 'MidnightBlue', 
                'background-color': 'BlanchedAlmond', 
                'border-color': 'MidnightBlue',
                'font-size': '15px'}
ERROR_STYLE = {'textAlign': 'center', 'color': 'FireBrick', 'margin-bottom' : 10}
SORT_LIST = [{'label': 'Alphabetical', 'value': 'alpha'},
                {'label': 'Ascending', 'value': 'sum ascending'},
                {'label': 'Descending', 'value': 'sum descending'}]
# may become non-static variable later:
cat_list = [{'label': 'Species', 'value': 'Species'},
                {'label': 'Subspecies', 'value': 'Subspecies'},
                {'label':'View', 'value': 'View'},
                {'label': 'Sex', 'value': 'Sex'},
                {'label': 'Hybrid Status', 'value':'hybrid_stat'}, 
                {'label': 'Locality', 'value': 'locality'}
                ]
DOCS_URL = "https://github.com/Imageomics/dashboard-prototype#how-it-works"

def get_hist_div(mapping):
    '''
    Function to generate the histogram options section of the dashboard, including button to select 'Map View'. 
    Provides choice of variables for distribution and to color by, with options for order to sort x-axis.

    Parameters:
    -----------
    mapping - Boolean. If False, does not render "Show Map View" button. 

    Returns:
    --------
    hist_div - HTML Div containing all user options for histogram (variable for distribution, coloring, and order to sort x-axis), plus and 'Map View' button.

    '''
    
    hist_div = [
        html.Div([
            html.H4("Show me the distribution of ...", style = H4_STYLE),
            # Add dropdown options
            # x-axis (feature) distribution options: 'Subspecies', 'Locality'
            dcc.RadioItems(cat_list[:2] + cat_list[5:], 
                        'Subspecies',
                        id = 'x-variable')
            ], style = HALF_DIV_STYLE
            ),
            
        html.Div([
            html.H4("Colored by ...", style = H4_STYLE),
        #select color-by option: 'View', 'Sex', 'Hybrid Status'
            dcc.RadioItems(cat_list[2:-1],
                            'View',
                            id = 'color-by')
            ], style = HALF_DIV_STYLE
        ),
        
        html.Div([
        html.H4("Sort distribution ", style = {'color': 'MidnightBlue', 'margin-top' : 10, 'margin-bottom' : 10}),
        dcc.RadioItems(SORT_LIST,
                        'alpha',
                        id = 'sort-by',
                        inline = True)
                ], style = HALF_DIV_STYLE
        )]
    
    if mapping:
        button_div = html.Div([
            # Button to switch to Map View
            html.Button("Show Map View",
                        style = BUTTON_STYLE,
                        id = 'dist-view-btn',
                        n_clicks = 0)
                 ], style = HALF_DIV_STYLE
            )
    else:
        # No mapping info, so no Map View button   
        button_div = html.Div([
                ], 
                id = 'dist-view-btn',
                style = HALF_DIV_STYLE
        )
    hist_div.append(button_div)
       
    return hist_div

def get_map_div():
    '''
    Function to generate the mapping options section of the dashboard. 
    Provides choice of variables to color by and button to switch back to histogram ('Show Histogram').

    Returns:
    --------
    map_div - HTML Div containing all user options for map (variables for coloring) and 'Show Histogram' button.

    '''
    map_div = [
        html.Div([
            html.H4('''
                    This map shows the distribution of samples by locality, 
                    where the size of the dots is determined by the total number of samples at that location.
                    ''', 
                    id = 'x-variable', #label to avoid nonexistent callback variable
                    style = {'color': 'MidnightBlue', 'margin-left': 20, 'margin-right': 20}
                )
            ], style = {'width': '48%', 'display': 'inline-block', 'vertical-align': 'bottom'}
            ),
            
        html.Div([
            html.H4("Colored by ...", style = H4_STYLE),
            #select color-by option: 'Species', 'Subspecies', 'View', 'Sex', 'Hybrid Status', 'Locality'
            dcc.RadioItems(cat_list,
                            'View',
                            id = 'color-by',
                            style = {'padding-right': '20%', 
                                     'display': 'inline-flex', 
                                     'flex-wrap': 'wrap', 
                                     'flex-direction': 'row', 
                                     'justify-content': 'space-between'})
            ], style = {'width': '48%', 'display': 'inline-block', 'margin-bottom': 20}
        ),

       html.Div([
               ], 
               id = 'sort-by', #label sort-by box to avoid non-existent label and generate box so button doesn't move between views
               style = HALF_DIV_STYLE
        ), 
        html.Div([
        # Distribution View Type Button
        html.Button("Show Histogram",
                    style = BUTTON_STYLE,
                    id = 'dist-view-btn',
                    n_clicks = 0)
                ], style = HALF_DIV_STYLE
        )
    ]
    
    return map_div

def get_img_div(df, all_species, img_url):
    '''
    Function to generate the Image Sampling options section of the dashboard, including button to display images. 
    Provides empty list if no URLS are provided in the DataFrame for the entries.

    Parameters:
    -----------
    df - DataFrame with relevant data for display.
    all_species - All available species options for get_image dropdown.
    img_url - Boolean. If False, does not render "Data Sample Image Selection" section of Dashboard. 

    Returns:
    --------
    img_div - HTML Div containing all user options for sample image selection. Returns an empty list if no image urls available (img_url is False).

    '''
    if img_url:
        img_div =[
                    html.H1("Data Sample Image Selection", style = H1_STYLE),

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
                                style = BUTTON_STYLE,
                                id = 'display-img',
                                n_clicks = 0),

                    # Add some space after the button
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    # Image Should appear
                    html.Div(id = 'image-1')
        ]
    else:
        img_div = []
    return img_div

def get_main_div(hist_div, img_div):
    '''
    Function to return main div based on upload of data.

    Parameters:
    -----------
    hist_div - HTML Div for histogram view.
    img_div - HTML Div for sample image selector.

    Returns:
    --------
    main_div - HTML Div containing all user options, graphs, and image return.
    '''
    main_div = html.Div([
        html.H1("Data Distribution Statistics", style = H1_STYLE),

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
            dcc.Loading(id = 'dist-plot-loading',
                            type = "circle",
                            color = 'DarkMagenta',
                            children = dcc.Graph(id = 'dist-plot'))], style = HALF_DIV_STYLE),
        html.Div([
            dcc.Graph(id = 'pie-plot')], style = HALF_DIV_STYLE),

        html.Hr(),
        
        html.Div(img_div),

        # Add some space after the image to push up
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),

    ])
    return main_div

def get_error_div(error_dict):
    '''
    Function to return appropriate error message if there's a problem uploading the selected file.

    Parameters:
    -----------
    error_dict - Dictionary containing information about the error. Potential keys are 'feature', 'type', 'unicode', and 'other'.

    Returns:
    --------
    error_div - Div with the corresponding error message.

    '''
    if 'feature' in error_dict.keys():
        feature = error_dict['feature']
        error_div = html.Div([
                            html.H3("Source data does not have '" + feature + "' column. ",
                                    style = ERROR_STYLE),
                            html.H4(["Please see the ",
                                        html.A("documentation",
                                                href=DOCS_URL,
                                                target='_blank',
                                                style = ERROR_STYLE),
                                        " for list of required columns."], 
                                        style = ERROR_STYLE)
                        ])
    elif 'type' in error_dict.keys():
        error_div = html.Div([
                            html.H4(["The source file is not a valid CSV format, please see the ",
                                     html.A("documentation", 
                                            href=DOCS_URL,
                                            target='_blank',
                                            style = ERROR_STYLE),
                                     "."],
                            style = ERROR_STYLE)
        ])
    elif 'unicode' in error_dict.keys():
        error_div = html.Div([
            html.H4("There was a UnicodeDecode error processing this file.",
                    style = ERROR_STYLE)
        ])
    else:
        error_div = html.Div([
            html.H4("There was an error processing this file.",
                    style = ERROR_STYLE)
        ])
    return error_div
