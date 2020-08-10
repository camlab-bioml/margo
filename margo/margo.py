import pandas as pd
import yaml


def lookup(row, features, alias_dict):
    # nicknames = row["nicknames"].values[0]
    # if isinstance(nicknames, str) and nicknames != "nan":
    #     alias = nicknames.split("|")
    # else:
    #     alias = []
    # alias.append(row["official gene symbol"].values[0])
    mks = row["Cell Marker"].values[0]
    mks = mks.split(",")
    mks = [m.strip() for m in mks]

    # for f in features:
    #     if f in alias:
    #         return pd.DataFrame([[f, row["cell type"].values[0]]])
    # return None
    mk_df = pd.DataFrame()
    for f in features:
        if (alias_dict is None) or (f not in alias_dict):
            if f in mks:
                mk_df = pd.concat([mk_df, pd.DataFrame([[f, row["Cell Type"].values[0]]])])
        else:
            alias = alias_dict[f]
            for m in mks:
                if m in alias:
                    mk_df = pd.concat([mk_df, pd.DataFrame([[f, row["Cell Type"].values[0]]])])
    return mk_df


def collapse_celltype(marker_mat: pd.DataFrame) -> pd.DataFrame:
    for t1 in range(len(marker_mat.columns)):
        type1 = marker_mat.columns[t1]
        for t2 in range(t1+1, len(marker_mat.columns)):
            type2 = marker_mat.columns[t2]
            if (type1 != "NA" and type2 != "NA" and 
                marker_mat[type1].equals(marker_mat[type2])):
                marker_mat = marker_mat.rename(columns={type1: f"{type1}/{type2}", 
                    type2: "NA"})
                type1 = f"{type1}/{type2}"
    if "NA" in marker_mat.columns:
        marker_mat = marker_mat.drop("NA", axis=1)
    return marker_mat


# def drop_zeros(marker_mat: pd.DataFrame) -> pd.DataFrame:
#     marker_mat = marker_mat[(marker_mat.sum(axis=1) != 0).values]
#     for ct in marker_mat.columns:
#         if marker_mat[ct].sum() == 0:
#             marker_mat = marker_mat.drop(ct, axis=1)
#     return marker_mat

def drop_n_marker(marker_mat: pd.DataFrame, n_marker) -> pd.DataFrame:
    if n_marker < 1:
        raise NotGeneratableError("<min_marker_per_celltype> should be greater or equal to 1.")
    for ct in marker_mat.columns:
        if marker_mat[ct].sum() < n_marker:
            marker_mat = marker_mat.drop(ct, axis=1)
    return marker_mat


def construct_marker_mat_from_db(features: list, 
    database: list, 
    alias_marker = None, 
    tissue = None,
    min_marker = 1,
) -> pd.DataFrame:
    if tissue is not None:
        tissue = tissue.split(",")

    alias_dict = None
    if alias_marker is not None:
        with open(alias_marker, "r") as stream:
            alias_dict = yaml.safe_load(stream)

    marker = pd.DataFrame()
    for db in database:
        # marker_db = pd.read_csv(db, sep="\t")
        # marker_db = marker_db[marker_db.species != "Mm"]
        marker_df = pd.read_csv(db)
        if tissue is not None:
            temp_df = pd.DataFrame()
            for t in tissue:
                temp_df = pd.concat([temp_df, marker_df[marker_df.Tissue == t]])
            marker_df = temp_df

        for r in range(marker_df.shape[0] - 1):
            new_row = lookup(marker_df[r:r+1], features, alias_dict)
            # if new_row is not None:
            #     marker = pd.concat([marker, new_row])
            marker = pd.concat([marker, new_row])
    if marker.shape == (0, 0):
        raise NotGeneratableError("<tissue> does not exist in the tissue list.")

    marker.columns = ["feature", "cell_type"]
    marker.index = list(range(marker.shape[0]))
    # print(marker)

    marker_mat = pd.DataFrame(data=0, index=list(set(marker["feature"])), columns=list(set(marker["cell_type"])))
    for i in marker.index:
        marker_mat[marker["cell_type"][i]][marker["feature"][i]] = 1
    
    marker_mat = collapse_celltype(marker_mat)
    marker_mat = drop_n_marker(marker_mat, min_marker)
    return marker_mat


def to_yaml(marker_mat: pd.DataFrame, name: str) -> None:
    type_marker = {}
    for ct in marker_mat.columns:
        features = [f for f in marker_mat.index if marker_mat[ct][f] == 1]
        type_marker[ct] = features
    marker = {"cell_type": type_marker}
    
    with open(name, 'w') as yam:
        yaml.dump(marker, yam, width=2000, default_flow_style=False)
    

class NotGeneratableError(Exception):
    pass

# if __name__ == "__main__":
#     # exp_csv = "../BaselTMA_SP43_115_X4Y8.csv"
#     cell_marker = ["../marker_database/CellMarker-company.csv", 
#         "../marker_database/CellMarker-experiment.csv", 
#         "../marker_database/CellMarker-review.csv", 
#         "../marker_database/CellMarker-scs.csv"]
#     # alias_marker = "./marker_database/alias.yml"
# #     tissue = "Blood"
#     # exp_df = pd.read_csv(exp_csv, index_col=0)
#     # features = exp_df.columns

# #     # features = ["CD45", "CD3", "CD8"]
#     # marker_mat = construct_marker_mat_from_db(features=features, 
#     #     database=cell_marker, 
#     #     alias_marker=alias_marker,
#     #     tissue=tissue)
# #     # marker_mat = construct_marker_mat_from_db(features=features, database=cell_marker)
# #     # cd45 = [ct for ct in marker_mat.columns if marker_mat[ct]["CD45"] == 1]
# #     # print(cd45)
# #     # print(marker_mat)
# #     to_yaml(marker_mat, "./marker_yaml/celltype_marker_2.yml")
#     marker = pd.DataFrame()
#     for db in cell_marker:
#         # marker_db = pd.read_csv(db, sep="\t")
#         # marker_db = marker_db[marker_db.species != "Mm"]
#         marker_df = pd.read_csv(db)
#         marker = pd.concat([marker, marker_df["Tissue"]])
#     tissue = list(set(marker[0]))
#     tissue.sort()
#     print(tissue)
