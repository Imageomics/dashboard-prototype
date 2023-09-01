import json
import plotly
import pandas as pd
from components.divs import get_hist_div, get_map_div, get_img_div

def test_get_hist_div():
    # Test for "Show Map View" button
    output = get_hist_div(True)
    j_hist_div = json.dumps(output, cls = plotly.utils.PlotlyJSONEncoder)
    assert "Show Map View" in j_hist_div
   
    # Test without map button
    output2 = get_hist_div(False)
    j_hist_div_nobtn = json.dumps(output2, cls = plotly.utils.PlotlyJSONEncoder)
    assert "Show Map View" not in j_hist_div_nobtn


def test_get_map_div():    
    output = get_map_div()
    j_map__div = json.dumps(output, cls = plotly.utils.PlotlyJSONEncoder)
    # Check for proper button label
    assert "Show Histogram" in j_map__div


def test_get_img_div():
    # Define some test data
    data = {
            'Species': ['species1', 'species2', 'species2'],
            'Subspecies': ['subspecies1', 'subspecies2', 'subspecies4'],
            'View': ['ventral', 'ventral', 'dorsal'],
            'Sex': ['male', 'female', 'female'],
            'Hybrid_stat': ['subspecies synonym', 'valid subspecies', 'subspecies synonym']
        }
    df = pd.DataFrame(data = data)

    # Check for format/contents
    output = get_img_div(df, {'species1': ['subspecies1'], 'species2': ['subspecies2', 'subspecies4']}, True)
    j_img_div = json.dumps(output, cls = plotly.utils.PlotlyJSONEncoder)
    assert "Display Images" in j_img_div
    assert '["species1", "species2"]' in j_img_div
    assert '["ventral", "dorsal"]' in j_img_div
    assert '["male", "female"]' in j_img_div
    assert '["subspecies synonym", "valid subspecies"]' in j_img_div

    # Test for no img_urls (img_url = False)
    output2 = get_img_div(df, None, False)
    assert output2 == []
