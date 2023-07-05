import unittest
import pandas as pd
from components.query import get_species_options, get_data


class TestQuery(unittest.TestCase):
    def test_get_species_options(self):
        data = {
            'Species': ['melpomene', 'erato', 'metharme'],
            'Subspecies': ['subspecies1', 'subspecies2', 'subspecies3']
        }
        df = pd.DataFrame(data=data)
        result = get_species_options(df)
        self.assertEqual(result.keys(), set(["Melpomene", "Erato", "Any"]))
        self.assertEqual(result["Melpomene"].tolist(), ['Any-Melpomene', 'subspecies1'])
        self.assertEqual(result["Erato"].tolist(),['Any-Erato', 'subspecies2'])
        self.assertEqual(result["Any"].tolist(),
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
