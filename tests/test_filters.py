import base64
import json
import pandas as pd
from dashboard import parse_contents


# Generate test data
def generate_mock_upload(filepath):
    # Function to mock the output of dcc.Upload based on given file
    # Code to mimic output of dcc.Upload from https://stackoverflow.com/a/66425568
    with open(filepath, "rb") as file:
        decoded = file.read()

    content_bytes = base64.b64encode(decoded)
    content_string = content_bytes.decode('utf-8')

    content_type = "".join(["data:", 'text/csv', ";base64"])

    contents = "".join([content_type, ",", content_string])
    return contents


def test_parse_contents():
    # Test feature parsing pulls proper columns
    # Check with full columns expected
    filepath = "test_data/HCGSD_full_testNA.csv"
    contents = generate_mock_upload(filepath)
    output = parse_contents(contents, "HCGSD_full_testNA.csv")
    expected_columns = ['Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lat', 'lon', 
                        'file_url', 'Image_filename', 'locality', 'lat-lon', 
                        'Samples_at_locality', 'Species_at_locality', 'Subspecies_at_locality']

    output = json.loads(output)
    dff = pd.read_json(output['processed_df'], orient = 'split')
    assert all([ex_col == col for ex_col, col in zip(expected_columns, list(dff.columns))])
    assert output['mapping'] == True
    assert output['images'] == True

    # Check with missing mapping features (also missing image info)
    filepath2 = "test_data/HCGSD_test_no_mapping.csv"
    contents2 = generate_mock_upload(filepath2)
    output2 = parse_contents(contents2, "HCGSD_test_no_mapping.csv")
    expected_columns2 = ['Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lon',
                        'locality']
        # 'lon' in data, 'lat' not, 'lon' maintained                
    output2 = json.loads(output2)
    dff2 = pd.read_json(output2['processed_df'], orient = 'split')
    assert all([ex_col == col for ex_col, col in zip(expected_columns2, list(dff2.columns))])
    assert output2['mapping'] == False
    assert output2['images'] == False

    # Check with missing image URL information
    filepath3 = "test_data/HCGSD_testNA.csv"
    contents3 = generate_mock_upload(filepath3)
    output3 = parse_contents(contents3, "HCGSD_testNA.csv")
    expected_columns3 = ['Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lat', 'lon',
                        'Image_filename', 'locality', 'lat-lon',
                        'Samples_at_locality', 'Species_at_locality', 'Subspecies_at_locality']
    output3 = json.loads(output3)
    dff3 = pd.read_json(output3['processed_df'], orient = 'split')
    assert all([ex_col == col for ex_col, col in zip(expected_columns3, list(dff3.columns))])
    assert output3['mapping'] == True
    assert output3['images'] == False

    # Check with just missing mapping information
    filepath4 = "test_data/HCGSD_test_nolon.csv"
    contents4 = generate_mock_upload(filepath4)
    output4 = parse_contents(contents4, "HCGSD_testNA.csv")
    expected_columns4 = ['Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lat', 
                        'file_url', 'Image_filename', 'locality']
    output4 = json.loads(output4)
    dff4 = pd.read_json(output4['processed_df'], orient = 'split')
    assert all([ex_col == col for ex_col, col in zip(expected_columns4, list(dff4.columns))])
    assert output4['mapping'] == False
    assert output4['images'] == True

