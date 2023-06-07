import numpy as np

# Helper functions for Dashboard

def get_species_options(df):
    '''
    Function to pull in dataFrame and produce a dictionary of species options (Melpomene, Erato, and Any)
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