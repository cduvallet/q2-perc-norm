# ----------------------------------------------------------------------------
# Copyright (c) 2016--, Claire Duvallet.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Plugin, Metadata, MetadataColumn, Categorical
#from qiime2.metadata import MetadataColumn, Categorical
from q2_types.feature_table import FeatureTable, RelativeFrequency

import q2_perc_norm
from q2_perc_norm._percentile_normalize import percentile_normalize

plugin = Plugin(
    name='perc_norm',
    version=q2_perc_norm.__version__,
    website='http://www.github.com/cduvallet/q2-perc-norm',
    package='q2_perc_norm',
    citation_text=('Sean Gibbons, Claire Duvallet, and Eric Alm. '
                   '"Correcting for batch effects in case-control '
                   'microbiome studies". bioRxiv (2017) '
                   'https://doi.org/10.1101/165910'),
    description=('This QIIME 2 plugin performs a model-free normalization '
                 'procedure where features (i.e. bacterial taxa) in case '
                 'samples are converted to percentiles of the equivalent '
                 'features in control samples within a study prior to pooling data across studies.'),
    short_description='Plugin to percentile-normalize case-control data.',
    user_support_text=('Raise an issue on the github repo: https://github.com/cduvallet/q2-perc-norm')
)

#TODO
# - maybe: define a new FeatureTable[PercentileNormalized] SemanticType and update in the output
# - add filters and related optional parameters (e.g. minimum number of controls, minimum detection rate within controls or cases)

plugin.methods.register_function(
    function=percentile_normalize,
    inputs={'table': FeatureTable[RelativeFrequency]
    },
    outputs=[('perc_norm_table', FeatureTable[RelativeFrequency])],
    input_descriptions={
        'table': ('The feature table containing the samples which will be '
                  'percentile normalized.')
    },
    parameters={'metadata': MetadataColumn[Categorical]
    },
    parameter_descriptions={
        'metadata': ('Sample metadata column which has samples '
                     'labeled as "case" or "control". Samples which '
                     'are not labeled are not included in the output table.')
    },
    output_descriptions={'perc_norm_table': 'The percentile-normalized OTU table.'},
    name='Percentile normalization',
    description=('Converts OTUs in case samples to percentiles of their '
                 'distribution in controls.')
)
