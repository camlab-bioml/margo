import csv
import gzip
import os
import sys
from typing import Optional

import pandas as pd
import requests
import yaml
from fake_useragent import UserAgent

from settings import ALIAS, ALIAS_MANUAL, DATABASES, LOCAL_DATABASES

# parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, parent)


# root_path = os.path.join(os.path.dirname(__file__), "..")


def generate_panglao_alias(row: pd.DataFrame, alias_dict: dict) -> None:
    alias = row["nicknames"]
    marker = row["marker"]
    # if isinstance(alias, float):
    #     alias_dict[marker]] = []
    #     return
    if not isinstance(alias, float):
        alias = alias.split("|")
        for a in alias:
            alias_dict[a] = marker
    # if marker in alias_dict:
    #     alias_dict[marker].extend(alias)
    #     alias_dict[marker] = list(set(alias_dict[marker]))
    # else:
    #     alias_dict[marker] = alias
    alias_dict[marker] = marker

def generate_cellmarker_alias(row: pd.DataFrame, alias_dict: dict) -> None:
    markers = row["marker"].split(",")
    for m in markers:
        if m not in alias_dict:
            alias_dict[m] = m

def generate_alias_marker(marker: pd.DataFrame, db: str) -> None:
    alias_dict = {}
    with open(ALIAS, "r") as stream:
        alias_dict = yaml.safe_load(stream)
    if db == "panglao":
        marker.apply(generate_panglao_alias, axis=1, alias_dict=alias_dict)
    if db == "cellmarker":
        marker.apply(generate_cellmarker_alias, axis=1, alias_dict=alias_dict)
        # for r in range(marker.shape[1]):
        #     generate_cellmarker_alias(marker[r, r+1], alias_dict)
    # print(alias_dict)
    if db == "manual":
        with open(ALIAS_MANUAL, 'r') as stream:
            alias_manual = yaml.safe_load(stream)
            for key, val in alias_manual.items():
                # if key in alias_dict:
                #     alias_dict[key].extend(val)
                # else:
                #     alias_dict[key] = val
                alias = val + [key]
                marker = key
                for a in alias:
                    if a in alias_dict:
                        marker = alias_dict[a]
                for a in alias:
                    alias_dict[a] = marker
    # for key, val in alias_dict.items():
    #     alias_dict[key] = list(set(alias_dict[key]+[key]))
    with open(ALIAS, "w") as stream:
        yaml.dump(alias_dict, stream, width=80, default_flow_style=False)


def process_panglao() -> None:
    # path = LOCAL_DATABASES["panglao"]
    path = "margo/marker_database/PanglaoDB_markers_27_Mar_2020.tsv"
    marker = pd.read_csv(path, error_bad_lines=False, sep="\t")
    marker = marker[(marker["species"] == "Mm Hs") | (marker["species"] == "Hs")]
    new_marker = marker[["cell type", "official gene symbol", "organ", "nicknames"]]
    new_marker.columns = ["cell_type", "marker", "tissue", "nicknames"]

    generate_alias_marker(new_marker, "panglao")
    new_marker = new_marker.drop("nicknames", axis=1)
    j = lambda a: ",".join(a)
    new_marker = (
        new_marker.groupby(by="cell_type")
        .agg({"marker": j, "tissue": "first"})
        .reset_index()
    )
    # print(new_marker)
    new_marker.to_csv(path)


def process_cellmarker() -> None:
    path = LOCAL_DATABASES["cellmarker"]
    marker = pd.read_csv(path, error_bad_lines=False, sep="\t")
    new_marker = marker[["cellName", "cellMarker", "tissueType"]]
    new_marker.columns = ["cell_type", "marker", "tissue"]
    new_marker["marker"] = new_marker["marker"].str.replace(" ", "")
    generate_alias_marker(new_marker, "cellmarker")
    new_marker.to_csv(path)


def download_tsv_gz(name: str, url: str) -> None:
    temp_one = "margo/marker_database/temp.tsv.gz"
    out_path = LOCAL_DATABASES[name]
    ua = UserAgent()
    headers = {'User-Agent': str(ua.chrome)}
    r = requests.get(url, headers=headers, timeout=30)
    open(temp_one, "wb").write(r.content)
    with gzip.open(temp_one, "rb") as f_one:
        data = f_one.read()
        with open(out_path, "wb") as f_two:
            f_two.write(data)
    os.remove(temp_one)


def download_csv(name: str, url: str) -> None:
    out_path = LOCAL_DATABASES[name]
    r = requests.get(url, allow_redirects=True)
    open(out_path, "wb").write(r.content)


def download_databases(db_name: Optional[list] = None) -> None:
    if db_name is None:
        db_name = list(DATABASES.keys())
    for db in db_name:
        if db not in DATABASES:
            raise Exception(
                f"Margo currently doesn't support {db}, entre 'margo -h' for a list of supporting databases."
            )
        url = DATABASES[db]

        if db == "panglao":
            print("Database update failed. By terms and conditions of PabglaoDB, bot access is not permitted. If a later version is available, please contact Campbell Lab for manual update. Last updated version: PanglaoDB_markers_27_Mar_2020")
            # download_tsv_gz(db, url)
            # process_panglao()
        elif db == "cellmarker":
            download_csv(db, url)
            process_cellmarker()
            print("CellMarker Database successfully updated.")


# if __name__ == "__main__":
#     # print(DATABASES)
#     download_databases(['panglao', 'cellmarker'])
