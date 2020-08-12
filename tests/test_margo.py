import os
from unittest import TestCase

import pandas as pd
import numpy as np

from margo.margo import construct_marker_mat_from_db, to_yaml


class TestMargo(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMargo, self).__init__(*args, **kwargs)
        exp_df = pd.read_csv(
            os.path.join(os.path.dirname(__file__), "test-data/exp_data.csv"),
            index_col=0,
        )
        self._features = exp_df.columns
        self._database = [
            os.path.join(
                os.path.dirname(__file__), "../margo/marker_database/CellMarker-company.csv"
            ),
            os.path.join(
                os.path.dirname(__file__),
                "../margo/marker_database/CellMarker-experiment.csv",
            ),
            os.path.join(
                os.path.dirname(__file__), "../margo/marker_database/CellMarker-review.csv"
            ),
            os.path.join(
                os.path.dirname(__file__), "../margo/marker_database/CellMarker-scs.csv"
            ),
        ]
        self._alias = os.path.join(
            os.path.dirname(__file__), "../margo/marker_database/alias.yml"
        )

        self._database_df = pd.DataFrame()
        for db in self._database:
            self._database_df = pd.concat([self._database_df, pd.read_csv(db)])

    def test_empty_feature(self):
        marker_mat = construct_marker_mat_from_db(
            features=self._features, database=self._database, alias_marker=self._alias
        )
        self.assertTrue((marker_mat.sum(axis=0) > 0).all(), True)

    def test_min_marker(self):
        min_marker = np.random.randint(2, 5)
        marker_mat = construct_marker_mat_from_db(
            features=self._features,
            database=self._database,
            alias_marker=self._alias,
            min_marker=min_marker,
        )
        self.assertTrue((marker_mat.sum(axis=0) >= min_marker).all(), True)

    def test_tissue_selection(self):
        tissue = "Breast,Blood"
        tissues = tissue.split(",")
        marker_mat = construct_marker_mat_from_db(
            features=self._features,
            database=self._database,
            alias_marker=self._alias,
            min_marker=4,
            tissue=tissue,
        )
        types = marker_mat.index
        for ct in types:
            ct_db = self._database_df[self._database_df["Cell Type"] == ct]
            temp = sum([(ct_db["Tissue"] == t) for t in tissues])
            self.assertTrue((temp > 0).all())
