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

    fig.update_layout(title = {'text': f'Distribution of {x_var} Colored by {color_by}'})

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
    fig = px.scatter_geo(df,
                        lat = df.lat,
                        lon = df.lon,
                        projection = "natural earth",
                        custom_data = ["Samples_at_locality", "Species_at_locality", "Subspecies_at_locality"],
                        size = df.Samples_at_locality,
                        color = color_by,
                        color_discrete_sequence = px.colors.qualitative.Bold,
                        title = "Distribution of Samples")
    
    fig.update_geos(fitbounds = "locations",
                    showcountries = True, countrycolor = "Grey",
                    showrivers = True,
                    showlakes = True,
                    showland = True, landcolor = "wheat",
                    showocean = True, oceancolor = "LightBlue")
    
    fig.update_traces(hovertemplate = 
                        "Latitude: %{lat}<br>"+
                        "Longitude: %{lon}<br>" +
                        "Samples at lat/lon: %{customdata[0]}<br>" +
                        "Species at lat/lon: %{customdata[1]}<br>" +
                        "Subspecies at lat/lon: %{customdata[2]}<br>"
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

    pie_fig.update_layout(title = {'text': f'Percentage Breakdown of {var}'})

    return pie_fig
