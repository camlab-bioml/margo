import pandas as pd
import yaml
from typing import Optional, List


class MarkerGenerator:
    """ A yaml cell type to gene expression marker generator.
    """

    def __init__(
        self, expr_csv: str, database: List[str], alias_marker: Optional[str] = None
    ) -> None:
        """ Initialize MarkerGenerator.

        :param exp_csv: path to the input csv file
        :type exp_csv: str
        :param database: list of paths to the input database files
        :type database: str
        :param alias_marker: path to the input alias marker file, defaults to None
        :type alias_marker: str, optional
        """
        expr_df = pd.read_csv(expr_csv, index_col=0)
        self._features = expr_df.columns
        self._alias_dict = None
        if alias_marker is not None:
            with open(alias_marker, "r") as stream:
                self._alias_dict = yaml.safe_load(stream)
        self._database_df = self._construct_database(database)
        self._marker_mat = pd.DataFrame()

    def _lookup(self, row: pd.DataFrame) -> pd.DataFrame:
        """ Helper for building marker matrix.

        :param row: a single row to be checked
        :type row: pd.DataFrame
        :return: a single row to be added to the marker matrix
        :rtype: pd.DataFrame
        """
        mks = row["Cell Marker"].values[0]
        mks = mks.split(",")
        mks = [m.strip() for m in mks]

        mk_df = pd.DataFrame()
        for f in self._features:
            if (self._alias_dict is None) or (f not in self._alias_dict):
                if f in mks:
                    mk_df = pd.concat(
                        [
                            mk_df,
                            pd.DataFrame(
                                [
                                    [
                                        f,
                                        row["Cell Type"].values[0],
                                        row["Tissue"].values[0],
                                    ]
                                ]
                            ),
                        ]
                    )
            else:
                alias = self._alias_dict[f]
                for m in mks:
                    if m in alias:
                        mk_df = pd.concat(
                            [
                                mk_df,
                                pd.DataFrame(
                                    [
                                        [
                                            f,
                                            row["Cell Type"].values[0],
                                            row["Tissue"].values[0],
                                        ]
                                    ]
                                ),
                            ]
                        )
        return mk_df

    def _collapse_celltype(self) -> None:
        """ A helper to collapse cell types with the same features into one single type.
        """
        for t1 in range(len(self._marker_mat.columns)):
            type1 = self._marker_mat.columns[t1]
            for t2 in range(t1 + 1, len(self._marker_mat.columns)):
                type2 = self._marker_mat.columns[t2]
                if (
                    type1 != "NA"
                    and type2 != "NA"
                    and self._marker_mat[type1].equals(self._marker_mat[type2])
                ):
                    self._marker_mat = self._marker_mat.rename(
                        columns={type1: f"{type1}/{type2}", type2: "NA"}
                    )
                    type1 = f"{type1}/{type2}"
        if "NA" in self._marker_mat.columns:
            self._marker_mat = self._marker_mat.drop("NA", axis=1)

    def _drop_n_marker(self, n_marker: int) -> None:
        """ Helper to drop cell type markers with less than `n_marker` features.

        :param n_marker: the minimum amount of features needed for each cell type
        :type n_marker: int
        :raises NotGeneratableError: raised with `n_marker` is less than 1
        """
        if n_marker < 1:
            raise NotGeneratableError(
                "<min_marker_per_celltype> should be greater or equal to 1."
            )
        for ct in self._marker_mat.columns:
            if self._marker_mat[ct].sum() < n_marker:
                self._marker_mat = self._marker_mat.drop(ct, axis=1)

    def _construct_database(self, database: List[str]) -> pd.DataFrame:
        """ Helper for constructing database df.

        :param database: list of paths to the input database files
        :type database: str
        :return:  corresponding database
        :rtype: pd.DataFrame
        """
        marker = pd.DataFrame()
        for db in database:
            marker_df = pd.read_csv(db)
            # if tissue is not None:
            #     temp_df = pd.DataFrame()
            #     for t in tissue:
            #         temp_df = pd.concat([temp_df, marker_df[marker_df.Tissue == t]])
            #     marker_df = temp_df

            for r in range(marker_df.shape[0] - 1):
                new_row = self._lookup(marker_df[r : r + 1])
                marker = pd.concat([marker, new_row])
        if marker.shape == (0, 0):
            raise NotGeneratableError("<tissue> does not exist in the tissue list.")

        marker.columns = ["feature", "cell_type", "tissue"]
        marker.index = list(range(marker.shape[0]))
        return marker

    def construct_marker_mat_from_db(
        self, tissue: List[str] = None, min_marker: int = 1,
    ) -> None:
        """ The main function to construct marker matrix.

        :param tissue: specified tissue to be searched within, defaults to None
        :type tissue: str, optional
        :param min_marker: specified minimum amount of features for each cell type, defaults to 1
        :type min_marker: int, optional
        :raises NotGeneratableError: raised when `tissue` does not exist in the tissue list
        """
        if tissue is not None:
            marker_df = pd.DataFrame()
            for t in tissue:
                marker_df = pd.concat(
                    [marker_df, self._database_df[self._database_df.tissue == t]]
                )
        else:
            marker_df = self._database_df

        self._marker_mat = pd.DataFrame(
            data=0,
            index=list(set(marker_df["feature"])),
            columns=list(set(marker_df["cell_type"])),
        )
        for i in marker_df.index:
            self._marker_mat[marker_df["cell_type"][i]][marker_df["feature"][i]] = 1

        self._collapse_celltype()
        self._drop_n_marker(min_marker)

    def get_marker_dict(self) -> dict:
        """ Construct a marker dictionary.

        :return: the marker dictionary
        :rtype: dict
        """
        type_marker = {}
        for ct in self._marker_mat.columns:
            features = [
                f for f in self._marker_mat.index if self._marker_mat[ct][f] == 1
            ]
            type_marker[ct] = features
        return {"cell_type": type_marker}

    def get_marker_mat(self) -> pd.DataFrame:
        """ Getter for `self._marker_mat`.

        :raises Exception: raised when this function is called before the marker matrix is generated
        :return: `self._marker_mat`
        :rtype: pd.DataFrame
        """
        return self._marker_mat

    def to_yaml(self, name: str) -> None:
        """ Convert the marker dictionary into a yaml file.

        :param name: name of the output file
        :type name: str
        """
        marker = self.get_marker_dict()
        with open(name, "w") as yam:
            yaml.dump(marker, yam, width=80, default_flow_style=False)


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
