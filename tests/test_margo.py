import os
from unittest import TestCase

import numpy as np
import pandas as pd
import yaml
from margo import MarkerGenerator


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
                os.path.dirname(__file__),
                "../margo/marker_database/panglao_db.csv",
            ),
            os.path.join(
                os.path.dirname(__file__),
                "../margo/marker_database/cellmarker_db.csv",
            ),
        ]
        self._alias = os.path.join(
            os.path.dirname(__file__), "../margo/marker_database/alias.yml"
        )
        self._database_df = pd.DataFrame()
        for db in self._database:
            self._database_df = pd.concat([self._database_df, pd.read_csv(db)])

        self._mg = MarkerGenerator(
            os.path.join(os.path.dirname(__file__), "test-data/exp_data.csv"),
            ["panglao", "cellmarker"],
        )

    def test_empty_feature(self):
        self._mg.construct_marker_mat_from_db()
        marker_mat = self._mg.get_marker_mat()
        self.assertTrue((marker_mat.sum(axis=0) > 0).all(), True)

    def test_min_marker(self):
        min_marker = np.random.randint(2, 5)
        self._mg.construct_marker_mat_from_db(min_marker=min_marker,)
        marker_mat = self._mg.get_marker_mat()
        self.assertTrue((marker_mat.sum(axis=0) >= min_marker).all(), True)

    def test_tissue_selection(self):
        tissues = ["Breast", "Blood"]
        self._mg.construct_marker_mat_from_db(
            tissue=tissues, min_marker=4,
        )
        marker_mat = self._mg.get_marker_mat()
        types = marker_mat.index
        for ct in types:
            ct_db = self._database_df[self._database_df["cell_type"] == ct]
            temp = sum([(ct_db["Tissue"] == t) for t in tissues])
            self.assertTrue((temp > 0).all())

    def test_to_yaml(self):
        self._mg.construct_marker_mat_from_db(
            tissue=["Breast"], min_marker=3,
        )
        expected = self._mg.get_marker_dict()
        output_path = os.path.join(
            os.path.dirname(__file__), "test-data/test_output.yml"
        )
        self._mg.to_yaml(output_path)
        with open(output_path, "r") as stream:
            actual = yaml.safe_load(stream)
        self.assertEqual(expected, actual)

