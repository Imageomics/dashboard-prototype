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


# Define Test Cases 
test_cases = [
        {   # Check with full columns expected
            "filepath": "test_data/HCGSD_full_testNA.csv",
            "filename": "HCGSD_full_testNA.csv",
            "expected_columns": ['Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lat', 'lon', 
                                    'file_url', 'Image_filename', 'locality', 'lat-lon', 
                                    'Samples_at_locality', 'Species_at_locality', 'Subspecies_at_locality'],
            "expected_mapping": True,
            "expected_images": True
        },
        {   # Check with missing mapping features (also missing image info)
            "filepath": "test_data/HCGSD_test_no_mapping.csv",
            "filename": "HCGSD_test_no_mapping.csv",
            # 'lon' in data, 'lat' not, 'lon' maintained   
            "expected_columns": ['Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lon',
                                    'locality'],
            "expected_mapping": False,
            "expected_images": False
        },
        {   # Check with missing image URL information
            "filepath": "test_data/HCGSD_testNA.csv",
            "filename": "HCGSD_testNA.csv",
            "expected_columns": ['Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lat', 'lon',
                                    'Image_filename', 'locality', 'lat-lon',
                                    'Samples_at_locality', 'Species_at_locality', 'Subspecies_at_locality'],
            "expected_mapping": True,
            "expected_images": False
        },
        {   # Check with just missing mapping information
            "filepath": "test_data/HCGSD_test_nolon.csv",
            "filename": "HCGSD_test_nolon.csv",
            "expected_columns": ['Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lat', 
                                    'file_url', 'Image_filename', 'locality'],
            "expected_mapping": False,
            "expected_images": True
        },
        {   # Check with full columns expected, but lat/lon out of bounds (1 lat and 2 lon)
            "filepath": "test_data/HCGSD_test_latLonOOB.csv",
            "filename": "HCGSD_test_latLonOOB.csv",
            "expected_columns": ['Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lat', 'lon', 
                                    'file_url', 'Image_filename', 'locality', 'lat-lon', 
                                    'Samples_at_locality', 'Species_at_locality', 'Subspecies_at_locality'],
            "expected_mapping": True,
            "expected_images": True
        },
        {   # Check with full columns expected, but 'long' instead of 'lon'
            "filepath": "test_data/HCGSD_test_latLong.csv",
            "filename": "HCGSD_test_latLong.csv",
            "expected_columns": ['Species', 'Subspecies', 'View', 'Sex', 'hybrid_stat', 'lat', 'lon', 
                                    'file_url', 'Image_filename', 'locality', 'lat-lon', 
                                    'Samples_at_locality', 'Species_at_locality', 'Subspecies_at_locality'],
            "expected_mapping": True,
            "expected_images": True
        },
]

def test_parse_contents():
    # Test feature parsing pulls proper columns
    for case in test_cases:
        contents = generate_mock_upload(case['filepath'])
        output = parse_contents(contents, case['filename'])
        output = json.loads(output)
        dff = pd.read_json(output['processed_df'], orient = 'split')

        assert list(dff.columns) == case['expected_columns']
        assert output['mapping'] == case['expected_mapping']
        assert output['images'] == case['expected_images']

        if case['filename'] == "HCGSD_test_latLonOOB.csv":
            assert len(dff.loc[dff.lat == 'unknown']) == 1
            assert len(dff.loc[dff.lon == 'unknown']) == 2
