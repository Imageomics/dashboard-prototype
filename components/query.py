import pandas as pd
import numpy as np
from dash import html

IMAGES_BASE_URL = "https://github.com/Imageomics/dashboard-prototype/raw/main/test_data/images/"

# Helper functions for Dashboard

def get_data():
    '''
    Function to read in DataFrame and perform required manipulations: 
        - add 'lat-lon', `Samples_at_locality`, 'Species_at_locality', and 'Subspecies_at_locality' columns.
        - make list of categorical columns.

    Returns:
    --------
    df - DataFrame of CSV with added column of number of samples collected at each lat-lon pair.
    cat_list - List of categorical variables for RadioItems (pie chart and map).

    '''
    df = pd.read_csv("test_data/Hoyal_Cuthill_GoldStandard_metadata_cleaned.csv")
    df['lat-lon'] = df['lat'].astype(str) + '|' + df['lon'].astype(str)
    df["Samples_at_locality"] = df['lat-lon'].map(df['lat-lon'].value_counts()/2)

    # Count and record number of species and subspecies at each lat-lon
    for lat_lon in df['lat-lon']:
        species_list = ['{}'.format(i) for i in df.loc[df['lat-lon'] == lat_lon]['Species'].unique()]
        subspecies_list = ['{}'.format(i) for i in df.loc[df['lat-lon'] == lat_lon]['Subspecies'].unique()]
        df.loc[df['lat-lon'] == lat_lon, 'Species_at_locality'] = ", ".join(species_list)
        df.loc[df['lat-lon'] == lat_lon, 'Subspecies_at_locality'] = ", ".join(subspecies_list)

    # Dictionary of categorical values for graphing options    
    cat_list = [{'label': 'Species', 'value': 'Species'},
                    {'label': 'Subspecies', 'value': 'Subspecies'},
                    {'label':'View', 'value': 'View'},
                    {'label': 'Sex', 'value': 'Sex'},
                    {'label': 'Hybrid Status', 'value':'hybrid_stat'},
                    {'label': 'Additional Taxa Information', 'value':'addit_taxa_info'}, 
                    {'label': 'Locality', 'value': 'locality'}]

    return df, cat_list

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
    melpomene_subspecies = df.loc[df.Species == 'melpomene', 'Subspecies'].unique()
    erato_subspecies = df.loc[df.Species == 'erato', 'Subspecies'].unique()
    melpomene_subspecies = np.insert(melpomene_subspecies, 0, 'Any-Melpomene')
    erato_subspecies = np.insert(erato_subspecies, 0, 'Any-Erato')
    all_subspecies = np.insert(df.Subspecies.unique(), 0, 'Any')
    all_species = {
        'Melpomene': melpomene_subspecies,
        'Erato' : erato_subspecies,
        'Any' : all_subspecies
    }
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
    '''
    filenames = get_filenames(df, subspecies, view, sex, hybrid, num_images)
    if filenames == 0:
        #print("No Such Images. Please make another selection.")
        return html.H4("No Such Images. Please make another selection.", 
                    style = {"color":"MidnightBlue"})
    Imgs = []
    for filename in filenames:
        if 'D_lowres' in filename:    
            image_directory = "dorsal_images/"
        else:
            image_directory = "ventral_images/"
        #remove 'tif' from filename and replace with 'png' in url
        image_path = IMAGES_BASE_URL + image_directory + filename[:-3] + "png?raw=true"
        Imgs.append(html.Img(src = image_path))
    return Imgs

def get_filenames(df, subspecies, view, sex, hybrid, num_images):
    '''
    Funtion to randomly select the given number of filenames for images adhering to specified filters.
    
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
    filenames or 0 - List of filenames meeting specified conditions (the lesser of the requested amount or number available). 
                     Returns 0 if no matching values.
    '''
    if 'Any' in subspecies:
        if subspecies == 'Any':
            df_sub = df.copy()
        else:
            subspecies = subspecies.split('-')[1].lower()
            df_sub = df.loc[df.Subspecies == subspecies].copy()
    else:
        df_sub = df.loc[df.Subspecies.isin(subspecies)].copy()
    df_sub = df_sub.loc[df_sub.View.isin(view)]
    df_sub = df_sub.loc[df_sub.Sex.isin(sex)]
    df_filtered = df_sub.loc[df_sub.hybrid_stat.isin(hybrid)]
    max_imgs = len(df_filtered)
    if max_imgs > 0:
        if num_images == None:
            num = 1
        else:
            num = min(num_images, max_imgs)
        filenames = df_filtered.sample(num).Image_filename.astype('string').values
        #return list of filenames for min(user-selected, available) images randomly selected images from the filtered dataset
        return list(filenames)
    else:
        return 0
