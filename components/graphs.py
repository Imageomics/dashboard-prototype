import plotly.express as px

def make_hist_plot(df, x_var, color_by, sort_by):
    '''
    Generates interactive histogram of selected variable, with option of properties to color by and order in which to sort.
    
    Parameters:
    -----------
    df - DataFrame of specimens.
    x_var - Variable to plot distribution.
    color_by - Property to color the plot by.
    sort_by - Ordering of bar charts (Alphabetical, Ascending, or Descending).

    Returns: 
    --------
    fig - Histogram of the distribution of the requested variable.
    '''
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

    fig.update_layout(title = {'text': f'Distribution of {x_var} Colored by {color_by}'},
                      font = {'size': 16},
                      margin = {
                            'l': 30,
                            'r': 20,
                            't': 35,
                            'b': 20
                        })

    return fig

def make_map(df, color_by):
    '''
    Generates interactive map of species and subspecies by location.
    
    Parameters:
    -----------
    df - DataFrame of specimens.
    color_by - Selected categorical variable by which to color.

    Returns: 
    --------
    fig - Map of their locations.
    '''
    df = df.copy()
    # only use entries that have valid lat & lon for mapping
    df = df.loc[df['lat-lon'].str.contains('unknown') == False]
    fig = px.scatter_mapbox(df,
                        lat = "Lat",
                        lon = "Lon",
                        #projection = "natural earth",
                        custom_data = ["Samples_at_locality", "Species_at_locality", "Subspecies_at_locality"],
                        size = "Samples_at_locality",
                        color = color_by,
                        color_discrete_sequence = px.colors.qualitative.Bold,
                        title = "Distribution of Samples",
                        zoom = 1,
                        mapbox_style = "white-bg")
    
    fig.update_traces(hovertemplate = 
                        "Latitude: %{lat}<br>"+
                        "Longitude: %{lon}<br>" +
                        "Samples at lat/lon: %{customdata[0]}<br>" +
                        "Species at lat/lon: %{customdata[1]}<br>" +
                        "Subspecies at lat/lon: %{customdata[2]}<br>"
    )

    fig.update_layout(
        font = {'size': 16},
        margin = {
            'l': 20,
            'r': 20,
            't': 35,
            'b': 20
        },
        mapbox_layers = [{
            "below": "traces",
            "sourcetype": "raster",
            "sourceattribution": "Esri, Maxar, Earthstar Geographics, and the GIS User Community",
            "source": ["https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]
            # Usage and Licensing (ArcGIS World Imagery): https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer
            # Style: https://roblabs.com/xyz-raster-sources/styles/arcgis-world-imagery.json
        }]
    )

    return fig

def make_pie_plot(df, var):
    '''
    Generates interactive pie chart of dataset specimens with option of properties to color by.

    Parameters:
    -----------
    df - DataFrame of specimens.
    var - Selected categorical variable by which to color.
    
    Returns: 
    --------
    fig - Pie chart of the percentage breakdown of the `var` samples in the dataset.
    '''
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

    pie_fig.update_layout(title = {'text': f'Percentage Breakdown of {var}'},
                          font = {'size': 16},
                          margin = {
                                'l': 20,
                                'r': 20,
                                't': 35,
                                'b': 20
                            })

    return pie_fig
