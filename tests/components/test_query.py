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
            'Species': ['melpomene', 'melpomene', 'erato', 'melpomene', 'erato', 'species3'],
            'Subspecies': ['schunkei', 'nanna', 'erato', 'rosina_N', 'guarica', None],
            'lat': [-13.43, 5.25, 5.25, 9.9, 5.25, 9.9],
            'lon': [-70.38,  -55.25, -55.25, -83.73, -55.25, -55.25]
        }
        cat_list = [{'label': 'Species', 'value': 'Species'},
                    {'label': 'Subspecies', 'value': 'Subspecies'},
                    {'label':'View', 'value': 'View'},
                    {'label': 'Sex', 'value': 'Sex'},
                    {'label': 'Hybrid Status', 'value':'hybrid_stat'},
                    {'label': 'Locality', 'value': 'locality'}]
        features = ['Species', 'Subspecies', 'lat', 'lon']
        locality = ['-13.43|-70.38', '5.25|-55.25', '5.25|-55.25', '9.9|-83.73','5.25|-55.25', '9.9|-55.25']

        # Test with mapping = True (location data)
        df = pd.DataFrame(data = data)
        result_df, result_list = get_data(df, True, features)
        self.assertEqual(result_df['lat-lon'].tolist(), locality)
        self.assertEqual(result_df['locality'].tolist(), locality)
        self.assertEqual(result_df["Samples_at_locality"].tolist(), [1,3,3,1,3,1])
        self.assertEqual(result_df["Species_at_locality"].tolist(), ['melpomene', 'melpomene, erato', 'melpomene, erato', 'melpomene', 'melpomene, erato', 'species3'])
        self.assertEqual(result_df["Subspecies_at_locality"].tolist(), ['schunkei', 'nanna, erato, guarica', 'nanna, erato, guarica', 'rosina_N', 'nanna, erato, guarica', 'unknown'])
        self.assertEqual(result_list, cat_list)

        # Test with mapping = False (no location data)
        df2 = pd.DataFrame(data = {key: data[key] for key in ['Species', 'Subspecies']})
        result_df2, result2_list = get_data(df2, False, features[:2])
        #self.assertEqual('locality' not in result_df2.columns, True)
        self.assertEqual(result_df2['locality'].tolist(), ['unknown' for i in range(len(locality))])
        self.assertEqual(result_df2["Species"].tolist(), ['melpomene', 'melpomene', 'erato', 'melpomene', 'erato', 'species3'])
        self.assertEqual(result_df2["Subspecies"].tolist(), ['schunkei', 'nanna', 'erato', 'rosina_N', 'guarica', 'unknown'])
        self.assertEqual(result2_list, cat_list)

    def test_get_filenames(self):
        BASE_URL_V = "https://github.com/Imageomics/dashboard-prototype/raw/main/test_data/images/ventral_images/"
        BASE_URL_D = "https://github.com/Imageomics/dashboard-prototype/raw/main/test_data/images/dorsal_images/"
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
            'Image_filename': ['10428251_V_lowres.png', 
                               '10428328_V_lowres.png', 
                               '10428723_V_lowres.png', 
                               '10427968_D_lowres.png', 
                               '10428804_D_lowres.png'],
            'file_url': [BASE_URL_V,
                        BASE_URL_V,
                        BASE_URL_V,
                        BASE_URL_D,
                        BASE_URL_D]
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
                       '10428251_V_lowres.png', 
                       '10428804_D_lowres.png', 
                       '10428723_V_lowres.png', 
                       ['10428251_V_lowres.png', '10428328_V_lowres.png', '10427968_D_lowres.png']]
        test_paths = [0,
                      BASE_URL_V,
                      BASE_URL_D,
                      BASE_URL_V,
                      [BASE_URL_V,
                      BASE_URL_V,
                      BASE_URL_D,
                      ]
                      ]

        result, paths = get_filenames(df, test_subspecies[0], test_view[0], test_sex[0], test_hybrid[0], test_nums[0])
        self.assertEqual(result, test_images[0])
        self.assertEqual(paths, test_paths[0])
        for i in range(1,4):
            result, paths = get_filenames(df, test_subspecies[i], test_view[i], test_sex[i], test_hybrid[i], test_nums[i])
            self.assertEqual(result, [test_images[i]])
            self.assertEqual(paths, [test_paths[i]])
        result, paths = get_filenames(df, test_subspecies[4], test_view[4], test_sex[4], test_hybrid[4], test_nums[4])
        #check lists have same elements
        self.assertCountEqual(result, test_images[4])
        self.assertCountEqual(paths, test_paths[4])
