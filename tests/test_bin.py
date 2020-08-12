import unittest
import rootpath
import pandas as pd
import yaml
import os
import sys
import subprocess

# import torch
# import warnings

# #
# # module_path = rootpath.detect()
# # if module_path not in sys.path:
# #     sys.path.append(module_path)
# # print(sys.path)
# #
# # module_path = os.path.join(rootpath.detect(), "astir")
# # if module_path not in sys.path:
# #     sys.path.append(module_path)
# # print(sys.path)


class TestBinMargo(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestBinMargo, self).__init__(*args, **kwargs)
        self._exec_path = os.path.join(rootpath.detect(), "bin/margo")
        self._expr_csv = os.path.join(
            os.path.dirname(__file__), "test-data/exp_data.csv"
        )
        self._database = [
            os.path.join(
                os.path.dirname(__file__),
                "../margo/marker_database/CellMarker-company.csv",
            ),
            os.path.join(
                os.path.dirname(__file__),
                "../margo/marker_database/CellMarker-experiment.csv",
            ),
            os.path.join(
                os.path.dirname(__file__),
                "../margo/marker_database/CellMarker-review.csv",
            ),
            os.path.join(
                os.path.dirname(__file__), "../margo/marker_database/CellMarker-scs.csv"
            ),
        ]

    def test_basic_command(self):
        bash_command = "python -W ignore {} {} {}".format(
            self._exec_path,
            self._expr_csv,
            os.path.join(os.path.dirname(__file__), "test-data/test_output.yml"),
        )
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        self.assertIsNone(error)
