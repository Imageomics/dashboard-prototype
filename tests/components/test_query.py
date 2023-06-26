import unittest
import pandas as pd
from components.query import get_species_options


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
