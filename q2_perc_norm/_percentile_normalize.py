from q2_types.feature_table import FeatureTable, RelativeFrequency
from qiime2 import CategoricalMetadataColumn

def percentile_normalize(table: FeatureTable[RelativeFrequency],
                         metadata: CategoricalMetadataColumn) -> FeatureTable[RelativeFrequency]:

    # Define an empty function for testing.
    print("Nothing")

    return table
