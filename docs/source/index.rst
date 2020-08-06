.. mentor documentation master file, created by
   sphinx-quickstart on Wed Aug  5 09:18:37 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**************************
Documentation for Mentor
**************************
.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. Indices and tables
.. ==================
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

Mentor is a tool that generates yaml cell type marker which maps cell types to gene expression from csv gene expression files.

--------------
Installation
--------------
::

   pip install mentor

--------------
Usage
--------------
::

   mentor <input_csv> <output_yaml> -t/--tissue <specified_tissues> -m/--min_marker_per_celltype <min_marker_per_celltype>

**Notes:**

* ``<input_csv>`` is path to the csv file which contains gene expression data. It must includes the feature names (gene names) as the column names in the first row.
* ``<output_yaml>`` is path where the yaml file is to be outputed to. 
*  | ``<specified_tissues>`` is one or more specified tissues where the cell markers is to be searched for within. Multiple tissues should be separated by commas. For example: ``-t Blood,Breast``. If ``-t`` is not specified or specified with ``-t all``, all tissues are gonna be searched. Note that if a tissue name contains a white space, the user could add quotation marks the tissues to avoid error (e.g. ``-t 'Large intestine'``, ``-t 'Splenic red pulp,Vocal fold'``). 
   | Here's a list of available tissues: 
   
   ::

   'Abdominal adipose tissue', 'Adipose tissue', 'Adrenal gland', 'Adventitia', 
   'Airway epithelium', 'Alveolus', 'Amniotic fluid', 'Amniotic membrane', 
   'Antecubital vein', 'Anterior cruciate ligament', 'Artery', 'Ascites', 'Bladder', 
   'Blood', 'Blood vessel', 'Bone', 'Bone marrow', 'Brain', 'Breast', 
   'Bronchoalveolar system', 'Brown adipose tissue', 'Cartilage', 'Chorionic villus', 
   'Colon', 'Colorectum', 'Cornea', 'Corneal endothelium', 'Corneal epithelium', 
   'Corpus luteum', 'Decidua', 'Deciduous tooth', 'Dental pulp', 'Dermis', 
   'Dorsolateral prefrontal cortex', 'Duodenum', 'Embryo', 'Embryoid body', 
   'Embryonic brain', 'Embryonic prefrontal cortex', 'Embryonic stem cell', 'Endometrium', 
   'Endometrium stroma', 'Epithelium', 'Esophagus', 'Eye', 'Fat pad', 'Fetal brain', 
   'Fetal gonad', 'Fetal kidney', 'Fetal liver', 'Fetal pancreas', 'Foreskin', 
   'Gall bladder', 'Gastric corpus', 'Gastric epithelium', 'Gastric gland',
   'Gastrointestinal tract', 'Germ', 'Gingiva', 'Gonad', 'Gut', 'Hair follicle', 'Heart', 
   'Hippocampus', 'Inferior colliculus', 'Intervertebral disc', 'Intestinal crypt', 
   'Intestine', 'Jejunum', 'Kidney', 'Lacrimal gland', 'Large intestine', 
   'Laryngeal squamous epithelium', 'Larynx', 'Ligament', 'Limbal epithelium', 'Liver', 
   'Lung', 'Lymph', 'Lymph node', 'Lymphoid tissue', 'Mammary epithelium', 'Mammary gland', 
   'Meniscus', 'Midbrain', 'Molar', 'Muscle', 'Myocardium', 'Myometrium', 'Nasal concha', 
   'Nasal epithelium', 'Nerve', 'Nucleus pulposus', 'Optic nerve', 'Oral cavity', 
   'Oral mucosa', 'Osteoarthritic cartilage', 'Ovarian cortex', 'Ovarian follicle', 'Ovary', 
   'Oviduct', 'Pancreas', 'Pancreatic acinar tissue', 'Pancreatic islet', 'Parotid gland',
   'Periodontal ligament', 'Periosteum', 'Peripheral blood', 'Placenta', 'Plasma', 'Pleura', 
   'Pluripotent stem cell', 'Premolar', 'Primitive streak', 'Prostate', 'Pyloric gland', 
   'Rectum', 'Renal glomerulus', 'Retina', 'Retinal pigment epithelium', 'Salivary gland', 
   'Scalp', 'Sclerocorneal tissue', 'Seminal plasma', 'Serum', 'Sinonasal mucosa',
   'Skeletal muscle', 'Skin', 'Small intestinal crypt', 'Small intestine', 'Spinal cord', 
   'Spleen', 'Splenic red pulp', 'Sputum', 'Stomach', 'Subcutaneous adipose tissue', 
   'Submandibular gland', 'Sympathetic ganglion', 'Synovial fluid', 'Synovium', 'Tendon',
   'Testis', 'Thymus', 'Thyroid', 'Tongue', 'Tonsil', 'Tooth', 'Umbilical cord', 
   'Umbilical cord blood', 'Umbilical vein', 'Undefined', 'Urine', 'Uterus', 'Vagina', 
   'Venous blood', 'Visceral adipose tissue', 'Vocal fold', 'Whartons jelly', 
   'White adipose tissue'

* ``<min_marker_per_celltype>`` is the minimum number of markers a cell type needed to have in order to be included in the output. For example, if ``-m 3`` is indicated, each cell type in the output marker would have at least 3 expression markers. It is defaulted to 2 if not specified.





