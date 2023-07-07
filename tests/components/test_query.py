import unittest
import pandas as pd
from components.query import get_species_options, get_data, get_filenames


class TestQuery(unittest.TestCase):
    def test_get_species_options(self):
        data = {
            'Species': ['melpomene', 'erato', 'metharme'],
            'Subspecies': ['subspecies1', 'subspecies2', 'subspecies3']
        }
        df = pd.DataFrame(data=data)
        result = get_species_options(df)
        self.assertEqual(result.keys(), set(["Melpomene", "Erato", "Metharme", "Any"]))
        self.assertEqual(result["Melpomene"], ['Any-Melpomene', 'subspecies1'])
        self.assertEqual(result["Erato"],['Any-Erato', 'subspecies2'])
        self.assertEqual(result["Metharme"], ['Any-Metharme', 'subspecies3'])
        self.assertEqual(result["Any"],
                         ['Any', 'subspecies1', 'subspecies2', 'subspecies3'])
    
    def test_get_data(self):
        data = {
            'Species': ['melpomene', 'melpomene', 'erato', 'melpomene', 'erato'],
            'Subspecies': ['schunkei', 'nanna', 'erato', 'rosina_N', 'guarica'],
            'lat': [-13.43, 5.25, 5.25, 9.9, 5.25],
            'lon': [-70.38,  -55.25, -55.25, -83.73, -55.25]
        }
        cat_list = [{'label': 'Species', 'value': 'Species'},
                    {'label': 'Subspecies', 'value': 'Subspecies'},
                    {'label':'View', 'value': 'View'},
                    {'label': 'Sex', 'value': 'Sex'},
                    {'label': 'Hybrid Status', 'value':'hybrid_stat'},
                    {'label': 'Additional Taxa Information', 'value':'addit_taxa_info'}, 
                    {'label': 'Locality', 'value': 'locality'}]
        df = pd.DataFrame(data = data)
        result_df, result_list = get_data(df)
        self.assertEqual(result_df['lat-lon'].tolist(), ['-13.43|-70.38', '5.25|-55.25', '5.25|-55.25', '9.9|-83.73','5.25|-55.25'])
        self.assertEqual(result_df["Samples_at_locality"].tolist(), [1,3,3,1,3])
        self.assertEqual(result_df["Species_at_locality"].tolist(), ['melpomene', 'melpomene, erato', 'melpomene, erato', 'melpomene', 'melpomene, erato'])
        self.assertEqual(result_df["Subspecies_at_locality"].tolist(), ['schunkei', 'nanna, erato, guarica', 'nanna, erato, guarica', 'rosina_N', 'nanna, erato, guarica'])
        self.assertEqual(result_list, cat_list)

    def test_get_filenames(self):
        data = {
            'Species': ['melpomene', 'melpomene', 'erato', 'melpomene', 'erato'],
            'Subspecies': ['schunkei', 'nanna', 'erato', 'rosina_N', 'guarica'],
            'View': ['ventral', 'ventral', 'ventral', 'dorsal', 'dorsal',],
            'Sex': ['male', 'female', 'female', 'male', 'female'],
            'hybrid_stat': ['subspecies synonym', 
                            'valid subspecies', 
                            'subspecies synonym', 
                            'valid subspecies', 
                            'valid subspecies'],
            'Image_filename': ['10428251_V_lowres.tif', 
                               '10428328_V_lowres.tif', 
                               '10428723_V_lowres.tif', 
                               '10427968_D_lowres.tif', 
                               '10428804_D_lowres.tif']
        }
        df = pd.DataFrame(data = data)
        test_subspecies = ['Any', 
                           'Any-Melpomene', 
                           ['guarica'], 
                           'Any-Erato', 
                           ['schunkei', 'nanna', 'rosina_N']]
        test_view = [['dorsal'], 
                     ['ventral'], 
                     ['dorsal', 'ventral'], 
                     ['dorsal', 'ventral'], 
                     ['dorsal', 'ventral']]
        test_sex = [['male'], 
                    ['male'], 
                    ['male', 'female'], 
                    ['male', 'female'], 
                    ['male', 'female']]
        test_hybrid = [['unknown'], 
                       ['valid subspecies', 'subspecies synonym'], 
                       ['valid subspecies', 'subspecies synonym'], 
                       ['subspecies synonym'], 
                       ['valid subspecies', 'subspecies synonym']]
        test_nums = [1, 2, 1, None, 3]
        test_images = [0, 
                       '10428251_V_lowres.tif', 
                       '10428804_D_lowres.tif', 
                       '10428723_V_lowres.tif', 
                       ['10428251_V_lowres.tif', '10428328_V_lowres.tif', '10427968_D_lowres.tif']]
        result = get_filenames(df, test_subspecies[0], test_view[0], test_sex[0], test_hybrid[0], test_nums[0])
        self.assertEqual(result, test_images[0])
        for i in range(1,4):
            result = get_filenames(df, test_subspecies[i], test_view[i], test_sex[i], test_hybrid[i], test_nums[i])
            self.assertEqual(result, [test_images[i]])
        result = get_filenames(df, test_subspecies[4], test_view[4], test_sex[4], test_hybrid[4], test_nums[4])
        #check lists have same elements
        self.assertCountEqual(result, test_images[4])
