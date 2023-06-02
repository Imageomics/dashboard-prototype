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
python prototype-multiplot.py
```

Then navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) in your browser to see the graphs.


**Note:** `prototype_histogram.py` can be run in the same manner, but will only produce a histogram.

### Preview
![image](https://github.com/Imageomics/dashboard-prototype/assets/31709066/1a9e5f20-5565-43a4-bd80-fbb2b66bb507)
