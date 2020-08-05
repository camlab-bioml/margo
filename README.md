# MENTOR (MarkerGenerator)

A tool that generates yaml cell type marker which maps cell types to gene expression.    

## Installation

Install by running:
```
pip install mentor
```

## Documentation

Check out a full description of the project [here](https://to-be-done).

## Reference

Marker data extracted from *[CellMarker: a manually curated resource of cell markers in human and mouse.](https://academic.oup.com/nar/article/47/D1/D721/5115823) Nucleic Acids Research. 2018.* (Website: http://biocc.hrbmu.edu.cn/CellMarker).

---------------------------------------


<!-- A tool which extracts marker data from *[CellMarker: a manually curated resource of cell markers in human and mouse.](https://academic.oup.com/nar/article/47/D1/D721/5115823) Nucleic Acids Research. 2018.* (Website: http://biocc.hrbmu.edu.cn/CellMarker) and generates cell type marker.

Usage:
```
astir-marker <input_csv> <output_yaml> -t/--tissue <tissue> 
```
The first row of the `<input_csv>` csv file (as column names) should be the feature names (protein genes) of the single-cell data. 

The outputting yaml file `<output_yaml>` contains a dictionary as follow:
```
cell_type:
  Basal epithelial cell:
  - Vimentin
  - Cytokeratin 14
  - Cytokeratin 5
  Epithelial cell:
  - SMA
  - Cytokeratin 8/18
  Luminal epithelial cell:
  - Cytokeratin 8/18
  - Cytokeratin 19
  Myoepithelial cell:
  - Cytokeratin 14
  - SMA
  - CD44
  ```

If `<tissue>` is specified, the outputting yaml file will only extract cell type mapping within the corresponding tissue. Otherwise, the whole dataset would be searched. -->
