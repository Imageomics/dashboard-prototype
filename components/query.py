import numpy as np
from dash import html

# Helper functions for Dashboard

PRINT_STYLE = {"color": "MidnightBlue"}

def get_data(df, mapping, features):
    '''
    Function to read in DataFrame and perform required manipulations: 
        - fill null values in required columns with 'unknown'
        - add 'lat-lon', `Samples_at_locality`, 'Species_at_locality', and 'Subspecies_at_locality' columns.
        - make list of categorical columns.

    Parameters:
    -----------
    df - DataFrame of the data to visualize.
    mapping - Boolean. True when lat/lon are given in dataset.
    features - List of features (columns) included in the DataFrame. This is a subset of the suggested columns: 
                'Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lat', 'lon', 'file_url', 'Image_filename'
            
    Returns:
    --------
    df - DataFrame with added 'lat-lon' column and columns indicating number of samples collected at each lat-lon pair.
    cat_list - List of categorical variables for RadioItems (pie chart and map).

    '''
    # Dictionary of categorical values for graphing options  
    # Will likely choose to calculate and return this in later instance    
    cat_list = [{'label': 'Species', 'value': 'Species'},
                {'label': 'Subspecies', 'value': 'Subspecies'},
                {'label':'View', 'value': 'View'},
                {'label': 'Sex', 'value': 'Sex'},
                {'label': 'Hybrid Status', 'value':'hybrid_stat'},
                {'label': 'Locality', 'value': 'locality'}
    ]

    df = df.copy()
    df = df.fillna('unknown')
    features.append('locality')
    
    # If we don't have lat/lon, just return DataFrame with otherwise required features.
    if not mapping:
        if 'locality' not in df.columns:
            df['locality'] = 'unknown'
        return df[features], cat_list      
    
    # else lat and lon are in dataset, so process locality information
    df['lat-lon'] = df['lat'].astype(str) + '|' + df['lon'].astype(str)
    df["Samples_at_locality"] = df['lat-lon'].map(df['lat-lon'].value_counts()) # will duplicate if multiple views of same sample

    # Count and record number of species and subspecies at each lat-lon
    for lat_lon in df['lat-lon']:
        species_list = ['{}'.format(i) for i in df.loc[df['lat-lon'] == lat_lon]['Species'].unique()]
        subspecies_list = ['{}'.format(i) for i in df.loc[df['lat-lon'] == lat_lon]['Subspecies'].unique()]
        df.loc[df['lat-lon'] == lat_lon, "Species_at_locality"] = ", ".join(species_list)
        df.loc[df['lat-lon'] == lat_lon, "Subspecies_at_locality"] = ", ".join(subspecies_list)

    if 'locality' not in df.columns:
        df['locality'] = df['lat-lon'] # contains "unknown" if lat or lon null

    new_features = ['lat-lon', "Samples_at_locality", "Species_at_locality", "Subspecies_at_locality"]
    for feature in new_features:
        features.append(feature)

    return df[features], cat_list

def get_species_options(df):
    '''
    Function to pull in DataFrame and produce a dictionary of species options (Melpomene, Erato, and Any)

    Parameters:
    -----------
    df - DataFrame with image metadata.

    Returns:
    --------
    all_species - Dictionary of all potential species options and their subspecies.

    '''
    species_list = list(df.Species.unique())
    all_species = {}
    for species in species_list:
        subspecies_list = df.loc[df.Species == species, 'Subspecies'].unique()
        subspecies_list = np.insert(subspecies_list, 0 , 'Any-' + species.capitalize())
        all_species[species.capitalize()] = list(subspecies_list)
    all_subspecies = np.insert(df.Subspecies.unique(), 0, 'Any')
    all_species['Any'] = list(all_subspecies)
    
    return all_species

# Retrieve selected number of images

def get_images(df, subspecies, view, sex, hybrid, num_images):
    '''
    Function to retrieve the user-selected number of images.

    Parameters:
    -----------
    df - DataFrame with image metadata.
    subspecies - String. Subspecies of specimen selected by the user.
    view - String. View of specimen selected by the user.
    sex - String. Sex of specimen selected by the user.
    hybrid - String. Hybrid status of specimen selected by the user.
    num_images - Integer. Number of images requested by the user.

    Returns:
    --------
    Imgs - List of html image elements with `src` element pointing to paths for the requested number of images matching given parameters.
           Returns html header4 "No Such Images. Please make another selection." if no images matching parameters exist.
           Returns html header4 indicating number of matching entries without filename or filepath.
    '''
    try:
        filenames, filepaths = get_filenames(df, subspecies, view, sex, hybrid, num_images)
    except ValueError as e:
        return html.H4(str(e) + " Please make another selection.", 
                    style = PRINT_STYLE)
    Imgs = []
    for i in range(len(filenames)):
        if filenames[i] in filepaths[i]:
            image_path = filepaths[i]
        else:
            if filepaths[i][-1] == '/':
                image_path = filepaths[i] + filenames[i]
            else:
                image_path = filepaths[i] + '/' + filenames[i]
        Imgs.append(html.Img(src = image_path))
    return Imgs

def get_filenames(df, subspecies, view, sex, hybrid, num_images):
    '''
    Funtion to randomly select the given number of filenames for images adhering to specified filters.
    Raises ValueError indicating no such images if none match the user selections.
    
    Parameters:
    -----------
    df - DataFrame with image metadata.
    subspecies - String. Subspecies of specimen selected by the user.
    view - String. View of specimen selected by the user.
    sex - String. Sex of specimen selected by the user.
    hybrid - String. Hybrid status of specimen selected by the user.
    num_images - Integer. Number of images requested by the user. Defaults to 1 if no selection.

    Returns:
    --------
    filenames - List of filenames meeting specified conditions (the lesser of the requested amount or number available). 
    filepaths - List of filepaths (URLs) corresponding to the selected filenames. 
    
    '''
    if 'Any' in subspecies and type(subspecies) == str:
        if subspecies == 'Any':
            df_sub = df.copy()
        else:
            species = subspecies.split('-')[1].lower()
            df_sub = df.loc[df.Species == species].copy()
    else:
        df_sub = df.loc[df.Subspecies.isin(subspecies)].copy()
    df_sub = df_sub.loc[df_sub.View.isin(view)]
    df_sub = df_sub.loc[df_sub.Sex.isin(sex)]
    df_sub = df_sub.loc[df_sub.hybrid_stat.isin(hybrid)]

    num_entries = len(df_sub)
    # Filter out any entries that have missing filenames or URLs:
    df_sub = df_sub.loc[df_sub.Image_filename != 'unknown']
    df_sub = df_sub.loc[df_sub.file_url != 'unknown']
    max_imgs = len(df_sub)
    missing_vals = num_entries - max_imgs
    if max_imgs > 0:
        if num_images == None:
            num = 1
        else:
            num = min(num_images, max_imgs)
        df_filtered = df_sub.sample(num)
        filenames = df_filtered.Image_filename.astype('string').values
        filepaths = df_filtered.file_url.astype('string').values
        #return list of filenames for min(user-selected, available) images randomly selected images from the filtered dataset
        return list(filenames), list(filepaths)
    # If there aren't any images to display, check if there are no such entries or just missing information.
    elif missing_vals == 0:
        raise ValueError("No Such Images.")
    else:
        raise ValueError("No Such Images. Unknown filename(s) or path(s).")
