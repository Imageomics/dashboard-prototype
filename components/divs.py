from dash import html, dcc

# Fixed styles and sorting options
H1_STYLE = {'textAlign': 'center', 'color': 'MidnightBlue'}
H4_STYLE = {'color': 'MidnightBlue', 'margin-bottom' : 10}
HALF_DIV_STYLE = {'width': '48%', 'display': 'inline-block'}
QUARTER_DIV_STYLE = {'width': '24%', 'display': 'inline-block'}
SORT_LIST = [{'label': 'Alphabetical', 'value': 'alpha'},
                {'label': 'Ascending', 'value': 'sum ascending'},
                {'label': 'Descending', 'value': 'sum descending'}]
# may become non-static variable later:
cat_list = [{'label': 'Species', 'value': 'Species'},
                {'label': 'Subspecies', 'value': 'Subspecies'},
                {'label':'View', 'value': 'View'},
                {'label': 'Sex', 'value': 'Sex'},
                {'label': 'Hybrid Status', 'value':'hybrid_stat'},
                {'label': 'Additional Taxa Information', 'value':'addit_taxa_info'}, 
                {'label': 'Locality', 'value': 'locality'}
                ]

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
    if mapping:
        hist_div = [
            html.Div([
                html.H4("Show me the distribution of ...", style = H4_STYLE),
                # Add dropdown options
                # x-axis (feature) distribution options: 'Subspecies', 'Additional Taxa Information', 'Locality'
                dcc.RadioItems(cat_list[:2] + cat_list[5:], 
                            'Subspecies',
                            id = 'x-variable')
                ], style = HALF_DIV_STYLE
                ),
                
            html.Div([
                html.H4("Colored by ...", style = H4_STYLE),
            #select color-by option: 'View', 'Sex', 'Hybrid Status'
                dcc.RadioItems(cat_list[2:-2],
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
            ),
            html.Div([
            # Button to switch to Map View
            html.Button("Show Map View",
                        id = 'dist-view-btn',
                        n_clicks = 0)
                    ], style = HALF_DIV_STYLE
            )
            ]
        
    # No lat/lon in data so no Map View button
    else:
        hist_div = [
            html.Div([
                html.H4("Show me the distribution of ...", style = H4_STYLE),
                # Add dropdown options
                # x-axis (feature) distribution options: 'Subspecies', 'Additional Taxa Information', 'Locality'
                dcc.RadioItems(cat_list[:2] + cat_list[5:], 
                            'Subspecies',
                            id = 'x-variable')
                ], style = HALF_DIV_STYLE
                ),
                
            html.Div([
                html.H4("Colored by ...", style = H4_STYLE),
            #select color-by option: 'View', 'Sex', 'Hybrid Status'
                dcc.RadioItems(cat_list[2:-2],
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
            ),   
            # No mapping info, so no button   
            html.Div([
                    ], 
                    id = 'dist-view-btn',
                    style = HALF_DIV_STYLE
            )
        ]

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
            #select color-by option: 'Species', 'Subspecies', 'View', 'Sex', 'Hybrid Status', 'Additional Taxa Information', 'Locality'
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
                    id = 'dist-view-btn',
                    n_clicks = 0)
                ], style = HALF_DIV_STYLE
        )
    ]
    
    return map_div

def get_main_div(df, all_species, hist_div):
    '''
    Function to return main div based on upload of data.

    Parameters:
    -----------
    df - DataFrame with relevant data for display.
    all_species - All available species options for get_image dropdown.
    hist_div - HTML Div for histogram view.

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
            dcc.Graph(id = 'dist-plot')], style = HALF_DIV_STYLE),
        html.Div([
            dcc.Graph(id = 'pie-plot')], style = HALF_DIV_STYLE),

        html.Hr(),

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
    return main_div
