import os
from unittest import TestCase

import pandas as pd

from mentor.mentor import construct_marker_mat_from_db, to_yaml


class TestMentor(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMentor, self).__init__(*args, **kwargs)
        exp_df = pd.read_csv(os.path.join(
            os.path.dirname(__file__),"test-data/exp_data.csv"), index_col=0)
        self._features = exp_df.columns
        self._database = [os.path.join(
            os.path.dirname(__file__),"../marker_database/CellMarker-company.csv"), 
            os.path.join(
            os.path.dirname(__file__),"../marker_database/CellMarker-experiment.csv"), 
            os.path.join(
            os.path.dirname(__file__),"../marker_database/CellMarker-review.csv"), 
            os.path.join(
            os.path.dirname(__file__),"../marker_database/CellMarker-scs.csv")]
        self._alias = os.path.join(
            os.path.dirname(__file__),"../marker_database/alias.yml")

    def test_marker_mat_basic_construction(self):
        marker_mat = construct_marker_mat_from_db(features=self._features, 
            database=self._database, 
            alias_marker=self._alias)
        
