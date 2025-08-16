# ----------------------------------------------------------------------------
# Copyright (c) 2024, Claire Duvallet.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd
import pandas.testing as pdt

from qiime2.plugin.testing import TestPluginBase
from qiime2.plugin.util import transform
from q2_types.feature_table import BIOMV100Format

from q2_perc_norm._methods import duplicate_table


class DuplicateTableTests(TestPluginBase):
    package = 'q2_perc_norm.tests'

    def test_simple1(self):
        in_table = pd.DataFrame(
            [[1, 2, 3, 4, 5], [9, 10, 11, 12, 13]],
            columns=['abc', 'def', 'jkl', 'mno', 'pqr'],
            index=['sample-1', 'sample-2'])
        observed = duplicate_table(in_table)

        expected = in_table

        pdt.assert_frame_equal(observed, expected)

    def test_simple2(self):
        # test table duplication with table loaded from file this time
        # (for demonstration purposes)
        in_table = transform(
            self.get_data_path('table-1.biom'),
            from_type=BIOMV100Format,
            to_type=pd.DataFrame)
        observed = duplicate_table(in_table)

        expected = in_table

        pdt.assert_frame_equal(observed, expected)
