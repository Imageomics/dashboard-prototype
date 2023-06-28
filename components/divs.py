from dash import html, dcc

def get_hist_div(cat_list, sort_list, H4_style, div_style):
    '''
    Function to generate the histogram options section of the dashboard, including button to select 'Map View'. 
    Provides choice of variables for distribution and to color by, with options for order to sort x-axis.

    Parameters:
    -----------
    cat_list - List of categorical variables to be used for distribution and color-by options.
    sort_list - List of options for sorting x-axis of histogram.
    H4_style - Style setting for html Header 4.
    div_style - Style setting for div containers. 

    Returns:
    --------
    hist_div - HTML Div containing all user options for histogram (variable for distribution, coloring, and order to sort x-axis), plus and 'Map View' button.

    '''
    hist_div = [
        html.Div([
            html.H4("Show me the distribution of ...", style = H4_style),
            # Add dropdown options
            # x-axis (feature) distribution options: 'Subspecies', 'Additional Taxa Information', 'Locality'
            dcc.RadioItems(cat_list[:2] + cat_list[5:], 
                        'Subspecies',
                        id = 'x-variable')
            ], style = div_style
            ),
            
        html.Div([
            html.H4("Colored by ...", style = H4_style),
        #select color-by option: 'View', 'Sex', 'Hybrid Status'
            dcc.RadioItems(cat_list[2:-2],
                            'View',
                            id = 'color-by')
            ], style = div_style
        ),
        #html.Br(),
        html.Div([
        html.H4("Sort distribution ", style = {'color': 'MidnightBlue', 'margin-top' : 10, 'margin-bottom' : 10}),
        dcc.RadioItems(sort_list,
                        'alpha',
                        id = 'sort-by',
                        inline = True)
                ], style = div_style
        ),
        html.Div([
        #html.H4("Distribution View", style = {'color': 'MidnightBlue', 'margin-top' : 10, 'margin-bottom' : 10}),
        html.Button("Map View",
                    id = 'dist-view-btn',
                    n_clicks = 0)
                ], style = div_style
        )
        ]
    return hist_div

def get_map_div(cat_list, H4_style, div_style):
    '''
    Function to generate the mapping options section of the dashboard. 
    Provides choice of variables to color by and button to switch back to histogram ('Show Histogram').

    Parameters:
    -----------
    cat_list - List of categorical variables to be used for color-by options.
    H4_style - Style setting for html Header 4.
    div_style - Style setting for div containers.

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
            html.H4("Colored by ...", style = H4_style),
            #select color-by option: 'Species', 'Subspecies', 'View', 'Sex', 'Hybrid Status', 'Additional Taxa Information', 'Locality'
            dcc.RadioItems(cat_list,
                            'View',
                            id = 'color-by',
                            style = {'padding-right': '20%', 'display': 'inline-flex', 'flex-wrap': 'wrap', 'flex-direction': 'row', 'justify-content': 'space-between'})
            ], style = {'width': '48%', 'display': 'inline-block', 'margin-bottom': 20}
        ),
        #html.Br(),
       html.Div([
               ], 
               id = 'sort-by', #label sort-by box to avoid non-existent label and generate box so button doesn't move between views
               style = div_style
        ), 
        html.Div([
        # Distribution View Type Button
        html.Button("Show Histogram",
                    id = 'dist-view-btn',
                    n_clicks = 0)
                ], style = div_style
        )
    ]
    
    return map_div
