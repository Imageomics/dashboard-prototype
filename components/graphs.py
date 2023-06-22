import plotly.express as px


def make_map(df):
    '''
    Generates interactive graph of Species and Subspecies by location.
    
    Parameters:
    -----------
    df - dataframe of specimens

    Returns: 
    --------
    fig - Map of their locations
    '''
    fig = px.scatter_geo(df,
                        lat = df.lat,
                        lon = df.lon,
                        projection = "natural earth",
                        hover_data = ["Species", "Subspecies"],
                        size = df.samples_at_locality,
                        color = "Subspecies",
                        color_discrete_sequence = px.colors.qualitative.Bold)
    
    fig.update_geos(fitbounds = "locations",
                    showcountries = True, countrycolor = "Grey",
                    showrivers = True,
                    showlakes = True,
                    showland = True, landcolor = "wheat",
                    showocean = True, oceancolor = "LightBlue")
    
    return fig
