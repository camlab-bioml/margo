import os
from typing import List, Optional

import pandas as pd
import yaml
from difflib import SequenceMatcher

from margo.database import download_databases
from margo.data_reader import data_reading
from settings import ALIAS, LOCAL_DATABASES

# root_path = os.path.join(os.path.dirname(__file__), "..")


class MarkerGenerator:
    """ A yaml cell type to gene expression marker generator.
    """

    def __init__(
        self, path: str, database: List[str] = None, update_db: bool = False
    ) -> None:
        """ Initialize MarkerGenerator.

        :param exp_csv: path to the input csv file
        :type exp_csv: str
        :param database: list of databases
        :type database: List[str]
        :param alias_marker: path to the input alias marker file, defaults to None
        :type alias_marker: str, optional
        """
        self._features = data_reading(path)
        if update_db:
            download_databases(database)
        with open(ALIAS, "r") as stream:
            self._alias_dict = yaml.safe_load(stream)
        self._substitutions = {}
        self._process_feature_alias()
        self._database_df = self._construct_database(database)
        self._marker_mat = pd.DataFrame()

    def _similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def _process_feature_alias(self, threshold:float = 0.6) -> None:
        markers = list(self._alias_dict.keys())
        for i in range(len(self._features)):
            f = self._features[i]
            if f not in self._alias_dict:
                replace = None
                max_similarity = threshold
                for m in markers:
                    similarity = self._similar(f, m)
                    if similarity > max_similarity:
                        replace = m
                        max_similarity = similarity
                if replace is None:
                    self._substitutions[f] = "ignored"
                    self._features[i] = None
                else:
                    self._substitutions[f] = replace
                    self._features[i] = self._alias_dict[replace]
        # print(self._substitutions)
        # print(self._features)
        while None in self._features:
            self._features.remove(None)


    def _lookup_cellmarker(self, row: pd.DataFrame) -> pd.DataFrame:
        """ Helper for building marker matrix.

        :param row: a single row to be checked
        :type row: pd.DataFrame
        :return: a single row to be added to the marker matrix
        :rtype: pd.DataFrame
        """
        mks = row["marker"].values[0]
        mks = mks.split(",")

        mk_df = pd.DataFrame()
        for m in mks:
            if m in self._features:
                mk_df = pd.concat(
                    [
                        mk_df,
                        pd.DataFrame(
                            [
                                [
                                    m,
                                    row["cell_type"].values[0],
                                    row["tissue"].values[0],
                                ]
                            ]
                        ),
                    ]
                )

        return mk_df

        
        # for f in self._features:
        #   if f not in self._alias_dict:
        #         if f in mks:
        #             mk_df = pd.concat(
        #                 [
        #                     mk_df,
        #                     pd.DataFrame(
        #                         [
        #                             [
        #                                 f,
        #                                 row["cell_type"].values[0],
        #                                 row["tissue"].values[0],
        #                             ]
        #                         ]
        #                     ),
        #                 ]
        #             )
        #   else:
        #         for m in mks:
        #             if m in alias:
        #                 mk_df = pd.concat(
        #                     [
        #                         mk_df,
        #                         pd.DataFrame(
        #                             [
        #                                 [
        #                                     f,
        #                                     row["cell_type"].values[0],
        #                                     row["tissue"].values[0],
        #                                 ]
        #                             ]
        #                         ),
        #                     ]
        #                 )
        # return mk_df

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

    def _construct_database(
        self, database: Optional[List[str]]
    ) -> pd.DataFrame:
        """ Helper for constructing database df.

        :param database: list of paths to the input database files
        :type database: str
        :return:  corresponding database
        :rtype: pd.DataFrame
        """
        if database is None:
            database = list(LOCAL_DATABASES.keys())
        marker = pd.DataFrame()
        for db in database:
            if db not in LOCAL_DATABASES:
                raise Exception(
                    f"Margo currently doesn't support {db}, entre 'margo -h' for a list of supporting databases."
                )
            path = LOCAL_DATABASES[db]
            marker_df = pd.read_csv(path)

            for r in range(marker_df.shape[0] - 1):
                new_row = self._lookup_cellmarker(marker_df[r : r + 1])
                marker = pd.concat([marker, new_row])
        if marker.shape == (0, 0):
            raise NotGeneratableError("No matching gene name is found in database. Check gene naming format.")

        marker.columns = ["feature", "cell_type", "tissue"]
        marker.index = list(range(marker.shape[0]))
        return marker

    def construct_marker_mat_from_db(
        self, tissue: List[str] = None, min_marker: int = 2,
    ) -> None:
        """ The main function to construct marker matrix.

        :param tissue: specified tissue to be searched within, defaults to None
        :type tissue: str, optional
        :param min_marker: specified minimum amount of features for each cell type, defaults to 2
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

    def to_yaml(self, name: str, include_substitutions: bool=True) -> None:
        """ Convert the marker dictionary into a yaml file.

        :param name: name of the output file
        :type name: str
        """
        if name[-4:] != ".yml" and name[-5:] != ".yaml":
            raise(NotGeneratableError("Output file name must end by '.yml' or '.yaml'."))
        marker = self.get_marker_dict()
        with open(name, "w") as stream:
            yaml.dump(marker, stream, width=80, default_flow_style=False)
            print(f"Corresponding marker file generated as {name}.")
        if include_substitutions:
            if len(self._substitutions) > 0:
                substitutions_name = ''
                if name[-4:] == '.yml':
                    substitutions_name = name[:-4] + "_substitutions.yml"
                elif name[-5:] == '.yaml':
                    substitutions_name = name[:-5] + "_substitutions.yaml"
                with open(substitutions_name, "w") as stream:
                    yaml.dump(self._substitutions, stream, width=80, default_flow_style=False)
                    print(f"Some marker names cannot be found in the database and are ignored or substituted by a most similar one in the database. A list of substitutions could be checked at {substitutions_name}.")


class NotGeneratableError(Exception):
    pass


# if __name__ == "__main__":
#     mg = MarkerGenerator("../tests/test-data/exp_data.csv", ['panglao', 'cellmarker'])
#     mg.construct_marker_mat_from_db(["Immune system", 'Breast'], min_marker=3)
#     mg.to_yaml("../tests/test-data/test_output.yml")

##TODO: update available tissues
##TODO: update documentations
##TODO: update tests
