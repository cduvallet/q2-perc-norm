# ----------------------------------------------------------------------------
# Copyright (c) 2016--, Claire Duvallet.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2.plugin
from qiime2.plugin import Metadata, MetadataColumn, Categorical, SemanticType
from q2_types.feature_table import FeatureTable, RelativeFrequency, BIOMV210DirFmt

import q2_perc_norm
from q2_perc_norm._percentile_normalize import percentile_normalize

cites = qiime2.plugin.Citations.load('citations.bib',
    package='q2_perc_norm')

plugin = qiime2.plugin.Plugin(
    name='perc_norm',
    version=q2_perc_norm.__version__,
    website='http://www.github.com/cduvallet/q2-perc-norm',
    package='q2_perc_norm',
    citations=[cites['percnorm2018gibbons']],
    description=('This QIIME 2 plugin performs a model-free normalization '
                 'procedure where features (i.e. bacterial taxa) in case '
                 'samples are converted to percentiles of the equivalent '
                 'features in control samples within a study prior to pooling data across studies.'),
    short_description='Plugin for percentile-normalizing case-control data.',
    user_support_text=('Raise an issue on the github repo: https://github.com/cduvallet/q2-perc-norm')
)

# Define new output type
PercentileNormalized = SemanticType('PercentileNormalized',
    variant_of=FeatureTable.field['content'])

plugin.register_semantic_types(PercentileNormalized)

plugin.register_semantic_type_to_format(FeatureTable[PercentileNormalized],
    artifact_format=BIOMV210DirFmt)

# Register percentile normalize function (it's the only one so far)
plugin.methods.register_function(
    function=percentile_normalize,
    inputs={'table': FeatureTable[RelativeFrequency]
    },
    outputs=[('perc_norm_table', FeatureTable[PercentileNormalized])],
    input_descriptions={
        'table': ('The feature table containing the samples which will be '
                  'percentile normalized.')
    },
    parameters={'metadata': MetadataColumn[Categorical],
                'batch': MetadataColumn[Categorical],
                'n_control_thresh': qiime2.plugin.Int,
                'otu_thresh': qiime2.plugin.Float
    },
    parameter_descriptions={
        'metadata': ('Sample metadata column which has samples '
            'labeled as "case" or "control". Samples which '
            'are not labeled are not included in the output table.'),
        'batch': ('Optional: the sample metadata column which has '
            'different batches labeled. Batch labels do not need any '
            'specific format or value, but should be unique.'),
        'n_control_thresh': ('Minimum number of controls needed to '
            'perform percentile normalization. Because the transformation '
            'converts abundances in controls to a uniform distribution, '
            'we *highly* discourage performing percentile normalization '
            'on datasets with fewer than 30 controls, and certainly not '
            'fewer than 10 (the default value). If you have fewer controls '
            'than `N_control_thresh`, the normalization will return an error.'),
        'otu_thresh': ('OTU filtering threshold: an OTU must be present in at '
            'least `otu_thresh` fraction of cases OR controls, otherwise it '
            'gets thrown out and not percentile normalized. Percentile '
            'normalization does not perform well with very sparse OTUs, so '
            'we do not recommend lowering this threshold below 0.3. '
            'otu_thresh should be a value between 0 and 1 (inclusive).')
    },
    output_descriptions={
        'perc_norm_table': ('The percentile-normalized OTU table. '
            'If multiple batches were given, this table contains '
            'data which was percentile-normalized within each batch and '
            'then merged. Note that some OTUs may be filtered from certain '
            'batches if they are too infrequent within that batch. These '
            'will be NaN in the output OTU table.')},
    name='Percentile normalization',
    description=('Converts OTUs in case samples to percentiles of their '
                 'distribution in controls.')
)
