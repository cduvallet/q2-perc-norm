# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, Claire Duvallet.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages
import versioneer

# Setup copied from q2-emperor
setup(
    name="q2-perc-norm",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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
)
