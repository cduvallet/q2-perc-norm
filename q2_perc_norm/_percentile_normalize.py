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
                         metadata: qiime2.CategoricalMetadataColumn,
                         N_control_thresh: int=10,
                         otu_thresh: float=0.3) -> biom.Table:
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
    N_control_thresh : int [default=10]
        Minimum number of controls accepted to perform percentile
        normalization. Because the transformation converts abundances
        in controls to a uniform distribution, we *highly* discourage
        performing percentile normalization on datasets with fewer than
        30 controls, and certainly not fewer than 10 (the default value).
        If you have fewer controls than `N_control_thresh`, the
        normalization will return an error.
    otu_thresh : float [default=0.3]
        The OTU filtering threshold: OTUs must be present in at least
        otu_thresh fraction of cases OR controls, otherwise it gets thrown
        out and not percentile normalized. This method does not perform
        well with very sparse OTUs, so we do not recommend lowering
        this threshold below 0.3. otu_thresh should be [0, 1]

    Returns
    -------
    norm_biom : biom.Table
        A biom table with the normalized data, only including the samples
        that were labeled as either "case" or "control", and the OTUs
        which passed the otu_thresh threshold.
    """
    # Filter metadata to only include IDs present in the table.
    # Also ensures every distance table ID is present in the metadata.
    metadata = metadata.filter_ids(table.ids(axis='sample'))
    metadata = metadata.drop_missing_values()

    # filter the table to exclude samples that were dropped from
    # the metadata due to missing values
    table = table.filter(metadata.ids)

    metadata = metadata.to_series()

    ## Convert biom Table into dense pandas dataframe
    # Transpose so samples are in rows and OTUs/features in columns
    df = table.to_dataframe().to_dense().T

    # Get case and control samples from metadata
    control_samples = metadata[metadata == "control"].index.tolist()
    case_samples = metadata[metadata == "case"].index.tolist()

    # Make sure there are enough controls to perform normalization
    ## TODO: make this an optional parameter
    #N_control_thresh = 10
    if len(control_samples) < N_control_thresh:
        raise ValueError("There aren't enough controls in your data.")

    # Filter out OTUs which are not present in at least otu_thresh % of
    # cases OR controls
    ## TODO: make otu_thresh a user variable
    #otu_thresh = 0.3
    if otu_thresh > 0:
        perc_df = pd.DataFrame(
            index=df.columns,
            columns=['ctrls', 'cases'])
        perc_df['ctrls'] = \
            (df.loc[control_samples] != 0).sum() / len(control_samples)
        perc_df['cases'] = \
            (df.loc[case_samples] != 0).sum() / len(case_samples)
        keep_otus = perc_df\
            .query('(cases >= @otu_thresh) | (ctrls >= @otu_thresh)')\
            .index
        df = df[keep_otus]

    # Replace zeros with random draw from uniform(0, zero_val)
    ## TODO: make zero_val a user input
    #zero_val = 1e-9
    zero_val = df.min().min() / 10.0
    df = df.replace(0.0, np.nan)
    df_rand = pd.DataFrame(
        data=np.random.uniform(0.0, zero_val, size=(df.shape[0], df.shape[1])),
        index=df.index,
        columns=df.columns)
    df[pd.isnull(df)] = df_rand[pd.isnull(df)]

    # Using numpy is faster than pandas, so get the indices of samples
    control_indices = [df.index.get_loc(i) for i in control_samples]
    case_indices = [df.index.get_loc(i) for i in case_samples]

    all_samples = control_samples + case_samples
    all_indices = control_indices + case_indices

    ## Normalize control and case samples to percentiles of control distribution
    # j iterates over samples (rows), i iterates over OTUs/features (columns)
    x = df.values
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
