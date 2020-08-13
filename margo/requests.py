import os
import sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent)

import requests
from typing import Optional
from settings import DATABASES, LOCAL_DATABASES, ALIAS
import gzip, csv
import pandas as pd


def generate_single_alias(row: pd.DataFrame, alias_dict: dict) -> None:
    alias = row['nicknames'].values[0]
    if alias == 'NA':
        alias_dict[row['feature'].values[0]] = []
        return
    alias = alias.split('|')
    alias_dict[row['feature'].values[0]] = alias

def generate_alias_marker(marker: pd.DataFrame) -> None:
    alias_dict = {}
    marker.apply(generate_single_alias, axis=1, alias_dict=alias_dict)
    with open(f'../{ALIAS}', "w") as yam:
        yaml.dump(marker, yam, width=80, default_flow_style=False)

def process_panglo()
    path = LOCAL_DATABASE['panglo']
    marker = pd.read_csv(path)
    marker = marker[marker['species'] == 'Mm Hs' or marker['species'] == 'Hs']
    new_marker = marker[['cell type', 'official gene symbol', 'organ', 'nicknames']]
    new_marker.columns = ['cell_type', 'feature', 'tissue', 'nicknames']
    generate_alias_marker(new_marker)
    new_marker = new_marker.drop('nicknames', axis=1)
    new_marker.to_csv(path)

def process_cellmarker() -> None:
    path = LOCAL_DATABASE['cellmarker']
    marker = pd.read_csv(path)
    new_marker = marker[['cellName', 'cellMarker', 'tissueType']]
    new_marker.columns = ['cell_type', 'feature', 'tissue']
    new_marker.to_csv(path)

def download_tsv_gz(name:str, url:str) -> None:
    temp_name = 'marker_database/temp.tsv.gz'
    out_path = f'../{LOCAL_DATABASES[name]}'
    r = requests.get(url, allow_redirects=True)
    open(temp_name, 'wb').write(r.content)
    with gzip.open(temp_name, "rb") as f_in:
        with open(out_path, 'w') as f_out:
            read_tsv = csv.reader(f_in, delimiter="\t")
            for row in read_tsv:
                f_out.write(row)

def download_csv(name:str, url:str) -> None:
    out_path = f'../{LOCAL_DATABASES[name]}'
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
        elif url[-4:] == '.csv':
            download_csv(db, url)

        if db == 'panglo':
            process_panglo()
        elif db == 'cellmarker':
            process_cellmarker()
