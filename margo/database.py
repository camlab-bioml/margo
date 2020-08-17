import os
import sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent)

import requests
from typing import Optional
from settings import DATABASES, LOCAL_DATABASES, ALIAS
import gzip, csv
import pandas as pd
import yaml


root_path = os.path.join(os.path.dirname(__file__), '..')

def generate_single_alias(row: pd.DataFrame, alias_dict: dict) -> None:
    alias = row['nicknames']
    if isinstance(alias, float):
        alias_dict[row['marker']] = []
        return
    alias = alias.split('|')
    marker = row['marker']
    if marker in alias_dict:
        alias_dict[marker].extend(alias)
        alias_dict[marker] = list(set(alias_dict[marker]))
    else:
        alias_dict[marker] = alias

def generate_alias_marker(marker: pd.DataFrame) -> None:
    alias_dict = {}
    marker.apply(generate_single_alias, axis=1, alias_dict=alias_dict)
    # print(alias_dict)
    with open(os.path.join(root_path, ALIAS), "w") as yam:
        yaml.dump(alias_dict, yam, width=80, default_flow_style=False)

def process_panglao() -> None:
    path = os.path.join(root_path, LOCAL_DATABASES['panglao'])
    marker = pd.read_csv(path, error_bad_lines=False, sep='\t')
    marker = marker[(marker['species'] == 'Mm Hs') | (marker['species'] == 'Hs')]
    new_marker = marker[['cell type', 'official gene symbol', 'organ', 'nicknames']]
    new_marker.columns = ['cell_type', 'marker', 'tissue', 'nicknames']

    generate_alias_marker(new_marker)
    new_marker = new_marker.drop('nicknames', axis=1)
    j = lambda a: ",".join(a) 
    new_marker = new_marker.groupby(by='cell_type').agg({
                              'marker': j,
                              'tissue': 'first'}).reset_index()
    # print(new_marker)
    new_marker.to_csv(path)

def process_cellmarker() -> None:
    path = os.path.join(root_path, LOCAL_DATABASES['cellmarker'])
    marker = pd.read_csv(path, error_bad_lines=False, sep='\t')
    new_marker = marker[['cellName', 'cellMarker', 'tissueType']]
    new_marker.columns = ['cell_type', 'marker', 'tissue']
    new_marker.to_csv(path)

def download_tsv_gz(name:str, url:str) -> None:
    temp_name = os.path.join(root_path, 'margo/marker_database/temp.tsv')
    out_path = os.path.join(root_path, LOCAL_DATABASES[name])
    r = requests.get(url, allow_redirects=True)
    open(temp_name, 'wb').write(r.content)
    # with gzip.open(temp_name, "rb") as f_in:
    #     data = f_in.read()
    #     with open(out_path, 'wb') as f_out:
    #         f_out.write(data)
    #         read_tsv = csv.reader(f_in, delimiter="\t")
    #         for row in read_tsv:
    #             f_out.write(row)
    # os.remove(temp_name)

def download_csv(name:str, url:str) -> None:
    out_path = os.path.join(root_path, LOCAL_DATABASES[name])
    r = requests.get(url, allow_redirects=True)
    open(out_path, 'wb').write(r.content)

def download_databases(db_name: Optional[list]=None) -> None:
    if db_name is None:
        db_name = list(DATABASES.keys())
    for db in db_name:
        if db not in DATABASES:
            raise Exception(f"Margo currently doesn't support {db}, entre 'margo -h' for a list of supporting databases.")
        url = DATABASES[db]
        if url[-7:] == '.tsv.gz':
            download_tsv_gz(db, url)
        elif url[-4:] == '.csv' or url[-4:] == '.txt':
            download_csv(db, url)

        if db == 'panglao':
            process_panglao()
        elif db == 'cellmarker':
            process_cellmarker()


if __name__ == "__main__":
    # print(DATABASES)
    download_databases(['panglao', 'cellmarker'])
