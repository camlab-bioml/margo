.. margo documentation master file, created by
   sphinx-quickstart on Wed Aug  5 09:18:37 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**************************
Margo (Marker Generator)
**************************

Margo is a tool that generates yaml cell type marker which maps cell types to gene expression 
from csv gene expression files.

Checkout a full documentation `here <https://camlab-bioml.github.io/margo/>`_.

--------------
Installation
--------------
::

   pip install margo

--------------
Usage
--------------
::

   margo <input_csv> <output_yaml> -t/--tissue <specified_tissues> -m/--min_marker_per_celltype <min_marker_per_celltype>

The input file ``<input_csv>`` should be a csv file which contains single cell gene expression data. 
It must includes the feature names (gene markers) as the column names in the first row. 

The output yaml file ``<output_yaml>`` is a marker which maps cell types to gene markers. 

Here's an example:

::

   cell_type:
      Angiogenic T cell:
         - CD3
         - CD31
      Basal epithelial cell:
         - Vimentin
         - Cytokeratin 14
         - Cytokeratin 5
      CD1C-CD141- dendritic cell:
         - CD45
         - CD68
      Cancer cell:
         - CD44
         - Cytokeratin 8/18
         - Her2
         - CD45
         - CD20
      Cancer stem cell:
         - CD44
         - c-Myc
      Epithelial cell:
         - Cytokeratin 19
         - Cytokeratin 8/18
         - SMA
      Hematopoietic stem cell:
         - CD44
         - CD45
      Leukocyte:
         - CD3
         - CD45
         - CD20
      Luminal epithelial cell:
         - Cytokeratin 19
         - Cytokeratin 8/18
      Myoepithelial cell:
         - CD44
         - SMA
         - Cytokeratin 14

------------
Reference
------------

Marker data was extracted from database |text|_ (Website: http://biocc.hrbmu.edu.cn/CellMarker).

.. _text: https://academic.oup.com/nar/article/47/D1/D721/5115823

.. |text| replace:: *CellMarker: a manually curated resource of cell markers in human and mouse. Nucleic Acids Research. 2018.*
