import pandas as pd
from components.query import get_data
from components.graphs import make_hist_plot, make_map, make_pie_plot

# Define test data
df = pd.read_csv("test_data/HCGSD_full_testNA.csv")
included_features = ['Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lat', 'lon', 'file_url', 'Image_filename']
processed_df, cat_list = get_data(df, True, included_features)

def test_make_hist_plot():
    # Histplot output
    output = make_hist_plot(processed_df, 'Species', 'View', 'alpha')
    assert output['data', 0].type == "histogram"
    # Check sort by `alpha`
    output_layout = output['layout', 'xaxis']
    assert output_layout['categoryorder'] == None

    # Check not sort by 'alpha' ('sum ascending')
    output2 = make_hist_plot(processed_df, 'Species', 'View', 'sum ascending')
    assert output2['data', 0].type == "histogram"
    output2_layout = output2['layout', 'xaxis']
    assert output2_layout['categoryorder'] == 'sum ascending'

def test_make_map():
    # Map plot output
    output = make_map(processed_df, "Species")
    output_data = output['data', 0]
    assert output_data.type == "scattermapbox"
    #test for uknowns in data and check it's proper type
    assert 'unknown' not in output_data['customdata']

def test_make_pie():
    # Pie plot output 
    output = make_pie_plot(processed_df, "Species")
    output_data = output['data', 0]
    assert output_data.type == "pie"
    # Not color by 'Subspecies' has 'percent+label' in 'textinfo'
    assert output_data['textinfo'] == 'percent+label'
    
    # Pie plot output (color by 'Subspecies')
    output2 = make_pie_plot(processed_df, "Subspecies")
    output2_data = output2['data', 0]
    assert output2_data.type == "pie"
    # Color by 'Subspecies' has 'Species' added to 'hovertemplate'
    assert output2_data['hovertemplate'] == 'Subspecies=%{label}<br>Species=%{customdata[0]}<extra></extra>'
