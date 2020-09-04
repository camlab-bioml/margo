import pandas as pd
import os
import subprocess
from typing import Optional, List
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
# root = os.path.dirname(__file__)

import anndata


def data_reading(file_path: str, arg: Optional[str] = None) -> List[str]:
    if file_path[-4:] == ".csv":
        return read_csv(file_path)
    elif file_path[-4:] == ".rds":
        return read_rds(file_path)
    elif file_path[-5:] == ".h5ad":
        return read_anndata(file_path, arg)
    
def read_csv(file_path: str) -> List[str]:
    """ Reads csv file and extract feature names.

    :param file_path: path to csv file
    :type file_path: str
    :return: extracted feature name
    :rtype: List[str]
    """
    return list((pd.read_csv(file_path, index_col=0)).columns)

def read_rds(file_path: str) -> List[str]:
    """ Reads SingleCellExperiment or Seurat object and extract feature names.

    :param file_path: path to corresponding rds file
    :type file_path: str
    :return: extracted features
    :rtype: List[str]
    """
    cache = 'margo/rds_cache.csv'
    cmd = ['Rscript', 'margo/rds_reader.R', file_path, cache]
    subprocess.call(cmd, cwd=os.getcwd())
    features = list((pd.read_csv(cache, index_col=0)).values[0])
    # print(features)
    os.remove(cache)
    return features

def read_anndata(file_path: str, protein: Optional[str]=None) -> List[str]:
    """ Reads .h5ad data and extracts feature names.

    :param file_path: path to corresponding h5ad file
    :type file_path: str
    :param protein: name of variable attr to find genes, defaults to None
    :type protein: Optional[str], optional
    :return: extracted features
    :rtype: List[str]
    """
    ad = anndata.read_h5ad(file_path)
    if protein == None:
        return list(ad.var_names)
    else:
        return list(ad.var[protein].values.T)


# if __name__ == "__main__":
#     print(read_rds("../tests/test-data/test_rds.rds"))
#     print(read_anndata("../tests/test-data/test_ann.h5ad", "protein"))