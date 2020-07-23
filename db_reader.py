import pandas as pd

def sanitize(row, features):
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

def construct_marker_mat_from_db(features):
    marker_db = pd.read_csv("./marker_database/PanglaoDB_markers.tsv", sep="\t")
    marker_db = marker_db[marker_db.species != "Mm"]

    marker = pd.DataFrame()
    for r in range(marker_db.shape[0] - 1):
        new_row = sanitize(marker_db[r:r+1], features)
        if new_row is not None:
            marker = pd.concat([marker, new_row])

    marker.columns = ["feature", "cell_type"]
    marker.index = list(range(marker.shape[0]))
    # print(marker)

    marker_mat = pd.DataFrame(data=0, index=features, columns=list(set(marker["cell_type"])))
    for i in marker.index:
        marker_mat[marker["cell_type"][i]][marker["feature"][i]] = 1
    return marker_mat

if __name__ == "__main__":
    exp_csv = "../BaselTMA_SP43_115_X4Y8.csv"
    exp_df = pd.read_csv(exp_csv, index_col=0)
    features = exp_df.columns
    print(construct_marker_mat_from_db(features))