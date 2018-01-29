from qiime2.plugin import Plugin
from qiime2.metadata import MetadataColumn, Categorical
from q2_types.feature_table import FeatureTable, RelativeFrequency

import q2_perc_norm
from q2_perc_norm._percentile_normalize import percentile_normalize

plugin = Plugin(
    name='Percentile normalization',
    version=q2_perc_norm.__version__,
    website='http://www.github.com/cduvallet',
    package='q2_perc_norm',
    citation_text=('Percentile normalization does stuff and is published somewhere...'),
    description=('This QIIME 2 plugin percentile-normalizes '
                 'case samples relative to controls.'),
    short_description='Plugin to percentile-normalize case-control data.',
    user_support_text=('Users should request support by raising issues '
                       'on the github repo.')
)

#TODO
# - define a new FeatureTable[PercentileNormalized] SemanticType and update in the output
# - figure out how the metadata file gets passed in (look at beta diversity)
# - figure out wtf MetadataColumn[Categorical] is (pandas series?)

plugin.methods.register_function(
    function=percentile_normalize,
    inputs={'table': FeatureTable[RelativeFrequency],
            'metadata': MetadataColumn[Categorical]
    },
    outputs=[('perc_norm_table', FeatureTable[RelativeFrequency])],
    input_descriptions={
        'table': ('The feature table containing the samples which will be '
                  'percentile normalized.'),
        'metadata': ('Categorical sample metadata column with "case" '
                     'and "control" labels.')
    },
    output_descriptions={'perc_norm_table': 'The percentile-normalized OTU table.'},
    name='Percentile normalization',
    description=('Converts OTUs in case samples to percentiles of their '
                 'distribution in controls.')
)
