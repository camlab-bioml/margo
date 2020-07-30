# MAGNETO (astir-MarkerGenerator)

A tool which extracts marker data from *[CellMarker: a manually curated resource of cell markers in human and mouse.](https://academic.oup.com/nar/article/47/D1/D721/5115823) Nucleic Acids Research. 2018.* (Website: http://biocc.hrbmu.edu.cn/CellMarker) and generates cell type marker mainly for the use of [astir](https://github.com/camlab-bioml/astir) classification.

Usage:
```
astir-marker <input_csv> <output_yaml> -t/--tissue <tissue> 
```
The inputting csv file `<input_csv>` should match [the format of astir csv input](https://www.camlab.ca/astir-doc/tutorials/notebooks/data_loading.html#2.-Loading-from-csv-and-yaml-files). In particular, the first row of the csv file (as column names) should be the feature names (protein genes) of the single-cell data. 

The outputting yaml file `<output_yaml>` would match the format as required by [astir marker](https://www.camlab.ca/astir-doc/tutorials/notebooks/getting_started.html#1.-Load-data) and so could be directly used for astir cell type classification.

If `<tissue>` is specified, the outputting yaml file will only extract cell type mapping within the corresponding tissue. Otherwise, the whole dataset would be searched.
