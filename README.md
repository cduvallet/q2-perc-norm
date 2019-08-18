# q2-perc-norm

QIIME 2 plugin for percentile normalization to correct for batch effects in microbiome case-control studies.

Read more about the method in our [paper](https://doi.org/10.1371/journal.pcbi.1006102) (Gibbons et al, PLOS Comp Bio 2018).

# Installing

You can install this plugin with conda or by cloning this repo and installing manually.
You need to have QIIME 2 version 2019.1 or later (though earlier versions of this plugin work with earlier versions of QIIME 2).
Also, regardless of which way you install, you need to be in a QIIME 2 environment for this to work.
[Install QIIME 2](https://docs.qiime2.org/2019.1/install/) and activate the QIIME 2 virtual environment (`source activate qiime2-2019.1`) before installing this plugin.

To install from conda, run:

```
conda install -c cduvallet q2_perc_norm
```

To install from this repo, clone the repo to your computer, `cd` into the main directory, and run:

```
python setup.py install
```

You can check that the installation worked by typing `qiime` on the command line.
The `perc-norm` plugin should show up in the list of available plugins.

# Using the plugin

The only method in this plugin is `percentile-normalize`, which percentile normalizes the abundance of OTUs in case samples with respect to their abundance in control samples.

## Preparing your data

You'll need to prepare your OTU table and metadata file for use with this plugin.
Your OTU table should be imported as a [QIIME 2 artifact](https://docs.qiime2.org/2019.1/concepts/#data-files-qiime-2-artifacts), with **OTUs in rows** and **samples in columns**.

Metadata should be a tab-delimited file with a column that contains samples labeled `case` and `control`.
It can also have a column that labels which batch each sample belongs to.
If this column is not specified, then percentile normalization is performed across all cases and controls provided in one go.

If your OTU table is already a QIIME 2 artifact, you can skip directly to running the code.
Otherwise, follow the instructions below to use your own tab-delimited OTU table.

### Notes on metadata and batch indicators

Your metadata file and the file that indicates which samples are in which batch don't need to be the same file (but can be the same). If you have two files, both need to have the sample IDs in the first column, and these IDs need to match the sample IDs in your OTU table.

The name of the column indicating the case/control status and the batch don't matter, because you specify them in your call to the percentile normalization function.

The values in the column indicating batches don't matter, as long as each batch gets a distinct value.

The values in the column indicating case or control status do matter, and need to be `case` or `control` exactly.

### Import tab-delimited OTU table into QIIME 2

You can use your own OTU table, or make a fake OTU table with `make_fake_data.py` in the `test_data/` folder here. This creates a fake OTU table and associated metadata file with case/control data (labeled in the "DiseaseState" column) from two different "experiments," labeled in the "batch" column.

If you're starting from a text file, you first need to convert the OTU table to biom format before you can import it into QIIME 2.

```
biom convert \
  -i test_otu_table.transpose.txt \
  -o test_otu_table.transpose.biom \
  --table-type="OTU table" \
  --to-hdf5
```

Once it's in biom format, you can import it into QIIME 2, turning it into an artifact:

```
qiime tools import \
  --input-path test_otu_table.transpose.biom \
  --type 'FeatureTable[RelativeFrequency]' \
  --source-format BIOMV210Format \
  --output-path test_otu_table.transpose.qza
```

## Run percentile normalization

You then run the `percentile-normalize` script from the `perc-norm` qiime plugin.

```
qiime perc-norm percentile-normalize \
  --i-table test_otu_table.transpose.qza \
  --m-metadata-file test_metadata.txt \
  --m-metadata-column DiseaseState \
  --o-perc-norm-table test_out.percentile_qiime.qza
```

If you have multiple batches in your metadata, you can also use the `--m-batch-file` and `--m-batch-column` flags to percentile normalize each batch separately.

```
qiime perc-norm percentile-normalize \
  --i-table test_otu_table.transpose.qza \
  --m-metadata-file test_metadata.txt \
  --m-metadata-column DiseaseState \
  --m-batch-file test_metadata.txt \
  --m-batch-column batch \
  --o-perc-norm-table test_out.percentile_qiime.qza
```

# To do's

* Update QIIME 2 downstream analyses to accept `FeatureTable[PercentileNormalized]`     
* Make tutorial showing how to percentile normalize multiple datasets
    - download multiple feature tables; add case/control and study columns in the metadata
    - merge the feature tables (and metadata tables, if possible) with q2-feature-table
    - percentile normalize the data with the batch handling
    - Note: I will probably not write this tutorial. If you are a user of q2-perc-norm and would like to write this, I would be very grateful!

# Versions

* 2019.4.1 - add more informative error in case "control" or "case" label is not found in the metadata
* 2019.4 - re-build package with Python 3.6, for compatibility with qiime 2019.1 release and later
* 2018.10 - fix conflicting PercentileNormalize type after qiime2 2018.8 release
* 2018.4.2 - allow Numeric metadata column to specify batch    
* 2018.4.1 - add multiple batch handling in `percentile-normalize`     
* 2018.4.0 - initial plugin

## Compatibilities

* q2-perc-norm versions 2018.* are not compatible with QIIME 2 versions 2019.* and later
* q2-perc-norm version 2018.10 and later are not compatible with QIIME 2 versions earlier than 2018.8
* q2-perc-norm versions 2018.4.* are not compatible with QIIME 2 versions
2018.8 or later

# Updating conda build

This is mostly a note to myself, if you are using this plugin then you can ignore this. This is the command to build an updated conda package:

```
conda-build recipe/ \
 -c qiime2/label/r2019.1 \
 -c conda-forge \
 -c bioconda \
 -c defaults \
 --override-channels \
 --python 3.6
```
