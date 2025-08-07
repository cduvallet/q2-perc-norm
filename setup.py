# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, Claire Duvallet.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages

# Setup copied from q2-emperor
setup(
    name="q2-perc-norm",
    version="2023.7.1",
    packages=find_packages(),
    author="Claire Duvallet",
    author_email="duvallet@mit.edu",
    description="Percentile-normalize data to correct for batch effects in case-control studies",
    license='BSD-3-Clause',
    url="https://qiime2.org",
    entry_points={
        'qiime2.plugins':
        ['q2-perc-norm=q2_perc_norm.plugin_setup:plugin']
    },
    zip_safe=False,
    package_data={
        'q2_perc_norm': ['citations.bib']
    }
)
