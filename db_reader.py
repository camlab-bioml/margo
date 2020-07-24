import pandas as pd


def lookup(row, features):
    nicknames = row["nicknames"].values[0]
    if isinstance(nicknames, str) and nicknames != "nan":
        alias = nicknames.split("|")
    else:
        alias = []
    alias.append(row["official gene symbol"].values[0])

    for f in features:
        if f in alias:
            return pd.DataFrame([[f, row["cell type"].values[0]]])
    return None


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
    marker_mat = marker_mat.drop("NA", axis=1)
    return marker_mat


def drop_zeros(marker_mat: pd.DataFrame) -> pd.DataFrame:
    marker_mat = marker_mat[(marker_mat.sum(axis=1) != 0).values]
    for ct in marker_mat.columns:
        if marker_mat[ct].sum() == 0:
            marker_mat = marker_mat.drop(ct, axis=1)
    return marker_mat


def construct_marker_mat_from_db(features: list, database: str) -> pd.DataFrame:
    marker_db = pd.read_csv(database, sep="\t")
    marker_db = marker_db[marker_db.species != "Mm"]

    marker = pd.DataFrame()
    for r in range(marker_db.shape[0] - 1):
        new_row = lookup(marker_db[r:r+1], features)
        if new_row is not None:
            marker = pd.concat([marker, new_row])

    marker.columns = ["feature", "cell_type"]
    marker.index = list(range(marker.shape[0]))
    # print(marker)

    marker_mat = pd.DataFrame(data=0, index=features, columns=list(set(marker["cell_type"])))
    for i in marker.index:
        marker_mat[marker["cell_type"][i]][marker["feature"][i]] = 1
    
    marker_mat = drop_zeros(marker_mat)
    marker_mat = collapse_celltype(marker_mat)
    return marker_mat


if __name__ == "__main__":
    exp_csv = "../BaselTMA_SP43_115_X4Y8.csv"
    panglao_db = "./marker_database/PanglaoDB_markers.tsv"
    exp_df = pd.read_csv(exp_csv, index_col=0)
    features = exp_df.columns
    marker_mat = construct_marker_mat_from_db(features=features, database=panglao_db)
    print(marker_mat.shape)
    print(marker_mat.columns)