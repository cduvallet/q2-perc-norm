# ----------------------------------------------------------------------------
# Copyright (c) 2016--, Claire Duvallet.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

# Data types
import biom
import qiime2

# Functions
import pandas as pd
import numpy as np
import scipy.stats as sp

def percentile_normalize(table: biom.Table,
                         metadata: qiime2.CategoricalMetadataColumn) -> biom.Table:
    """
    Converts an input table with cases and controls into percentiles
    of control samples.

    Parameters
    ----------
    table : biom.Table
        Feature table with relative abundances. Samples are in columns,
        features (i.e. OTUs) are in rows.
    metadata : qiime2.CategoricalMetadataColumn
        metadata column with samples labeled as "case" or "control".
        All samples with either label are returned, normalized to the
        equivalent percentile in "control" samples.

    Returns
    -------
    norm_biom : biom.Table
        A biom table with the normalized data, only including the samples
        that were labeled as either "case" or "control".
    """
    # Filter metadata to only include IDs present in the table.
    # Also ensures every distance table ID is present in the metadata.
    metadata = metadata.filter_ids(table.ids(axis='sample'))
    metadata = metadata.drop_missing_values()

    # filter the distance matrix to exclude samples that were dropped from
    # the metadata due to missing values
    table = table.filter(metadata.ids)

    metadata = metadata.to_series()

    ## Convert biom Table into dense pandas dataframe
    # Transpose to samples are in rows and OTUs/features in columns
    df = table.to_dataframe().to_dense().T
    x = df.values

    # Get case and control samples from metadata
    control_samples = metadata[metadata == "control"].index.tolist()
    case_samples = metadata[metadata == "case"].index.tolist()

    # TODO: make this an optional parameter
    N_control_thresh = 10
    if len(control_samples) < N_control_thresh:
        raise ValueError("There aren't enough controls in your data.")

    # TODO: perform filtering for OTU presence in X% of cases or controls

    # Using numpy is faster than pandas, so get the indices of samples
    control_indices = [df.index.get_loc(i) for i in control_samples]
    case_indices = [df.index.get_loc(i) for i in case_samples]

    all_samples = control_samples + case_samples
    all_indices = control_indices + case_indices

    ## Normalize control and case samples to percentiles of control distribution
    # j iterates over samples (rows), i iterates over OTUs/features (columns)
    norm_x = np.array(
        [
            [sp.percentileofscore(x[control_indices, i], x[j, i], kind='mean')
             for j in all_indices]
        for i in range(x.shape[1])
        ]).T

    ## Put back into dataframe and convert back to biom format
    # Transpose it as well, so that samples are back in columns
    norm_df = pd.DataFrame(
        data=norm_x,
        columns=df.columns,
        index=all_samples).T
    # Put this dataframe into biom format
    norm_biom = biom.Table(
        data=norm_df.values,
        observation_ids=norm_df.index,
        sample_ids=norm_df.columns)

    return norm_biom
