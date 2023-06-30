# Dashboard Prototype
Prototype data dashboard using the [Cuthill Gold Standard Dataset](https://datacommons.tdai.osu.edu/dataset.xhtml?persistentId=doi:10.5072/FK2/GZYWNV&version=DRAFT), which was processed from Cuthill, et. al. (original dataset available at [doi:10.5061/dryad.2hp1978](https://doi.org/10.5061/dryad.2hp1978)).


### How it works

Create and activate a new (python) virtual environment. 
Then install the required packages (if using `conda`, first run `conda install pip`):

``` 
pip install -r requirements.txt 
```

and run 

```
python dashboard.py
```

Then navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) in your browser to see the graphs.


### Preview

#### Histogram View
![image](dashboard_preview_hist.png)

#### Map View
![image](dashboard_preview_map.png)


### Running Tests

Within your python environment run the following command to run the tests:
```
python -m unittest
```
