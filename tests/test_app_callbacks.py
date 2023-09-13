import json
import plotly
from dashboard import update_dist_view, update_dist_plot, update_pie_plot, set_subspecies_options, update_display

# Define test data
data = {'processed_df': '{"columns":["Species","Subspecies","View","Sex","Hybrid_stat","Lat","Lon","lat-lon","Samples_at_locality","Species_at_locality","Subspecies_at_locality"],"index":[0,1,2,3,4,5,6,7,8,9],"data":[["erato","notabilis","unknown","unknown","subspecies synonym",-1.583333333,-77.75,"-1.583333333|-77.75",1,"erato","notabilis"],["erato","petiverana","ventral","male","valid subspecies",18.66666667,-96.98333333,"18.66666667|-96.98333333",1,"erato","petiverana"],["unknown","petiverana","ventral","male","valid subspecies","unknown",-84.68333333,"unknown|-84.68333333",1,"unknown","petiverana"],["erato","phyllis","dorsal","male","subspecies synonym",-27.45,-58.98333333,"-27.45|-58.98333333",1,"erato","phyllis"],["unknown","plesseni","ventral","male","valid subspecies",-1.4,"unknown","-1.4|unknown",1,"unknown","plesseni"],["melpomene","unknown","ventral","male","subspecies synonym",-13.36666667,-70.95,"-13.36666667|-70.95",1,"melpomene","unknown"],["melpomene","rosina_S","dorsal","male","valid subspecies",9.883333333,-83.63333333,"9.883333333|-83.63333333",1,"melpomene","rosina_S"],["erato","guarica","dorsal","female","valid subspecies",4.35,-74.36666667,"4.35|-74.36666667",1,"erato","guarica"],["melpomene","plesseni","ventral","male","subspecies synonym",-1.583333333,"unknown","-1.583333333|unknown",1,"melpomene","plesseni"],["melpomene","nanna","unknown","male","valid subspecies",-20.33333333,-40.28333333,"-20.33333333|-40.28333333",1,"melpomene","nanna"]]}',
        'all_species': {'Erato': ['Any-Erato', 'notabilis', 'petiverana', 'phyllis', 'guarica'], 'Unknown': ['Any-Unknown', 'petiverana', 'plesseni'], 'Melpomene': ['Any-Melpomene', 'unknown', 'rosina_S', 'plesseni', 'nanna'], 'Any': ['Any', 'notabilis', 'petiverana', 'phyllis', 'plesseni', 'unknown', 'rosina_S', 'guarica', 'nanna']}, 
        'mapping': True, 
        'images': True}
jsonified_data = json.dumps(data)


def test_update_dist_view_call():
    # Test hist div callback (no clicks or button)
    output = update_dist_view(0, [], jsonified_data)
    j_output = json.dumps(output, cls = plotly.utils.PlotlyJSONEncoder)
    assert "Show Map View" in j_output
    
    # Test map div callback (1 click and "Show Map View")
    output2 = update_dist_view(1, ["Show Map View"], jsonified_data)
    j_output2 = json.dumps(output2, cls = plotly.utils.PlotlyJSONEncoder)
    assert "Show Histogram" in j_output2

    # Test hist div callback (clicks and "Show Histogram")
    output3 = update_dist_view(2, children = "Show Histogram", jsonified_data = jsonified_data)
    j_output3 = json.dumps(output3, cls = plotly.utils.PlotlyJSONEncoder)
    assert "Show Map View" in j_output3


def test_update_dist_plot_call():
    # Check for proper type of fig (Histplot output)
    output = update_dist_plot('Species', 'View', 'alpha', "Show Map View", jsonified_data)
    assert output['data', 0].type == "histogram"
   
    # Map plot output
    output2 = update_dist_plot('Species', 'Subspecies', 'alpha', "Show Histogram", jsonified_data)
    assert output2['data', 0].type == "scattermapbox"


def test_update_pie_plot():
    output = update_pie_plot('Subspecies', jsonified_data)
    # Pie plot
    assert output['data', 0].type == "pie"


def test_subspecies_options():
    output = set_subspecies_options('Melpomene', jsonified_data)
    assert output == [{'label': i, 'value': i} for i in ['Any-Melpomene', 'unknown', 'rosina_S', 'plesseni', 'nanna']]


def test_update_display(mocker):
        mocker.patch('dashboard.get_images', return_value = ['image' + str(i) for i in range(5)])
        output = update_display(1, 
                                jsonified_data, 
                                ['notabilis', 'phyllis', 'guarica'],
                                ['dorsal', 'ventral'],
                                ['male', 'female'],
                                ['valid subspecies', 'subspecies synonym'],
                                5)
        assert len(output) == 5
        assert all([output[i] == ('image' + str(i)) for i in range(5)])
