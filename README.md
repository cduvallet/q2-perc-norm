# q2-perc-norm

QIIME 2 plugin for percentile normalization to correct for batch effects in microbiome case-control studies.

Read more about the method in our [paper](https://doi.org/10.1371/journal.pcbi.1006102) (Gibbons et al, PLOS Comp Bio 2018).

# Installing

You can install this plugin with conda or by cloning this repo and installing manually.
You need to have QIIME 2 version 2018.4 or later.
Also, regardless of which way you install, you need to be in a QIIME 2 environment for this to work.
[Install QIIME 2](https://docs.qiime2.org/2018.2/install/) and activate the QIIME 2 virtual environment (`source activate qiime2-2018.2`) before installing this plugin.

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
Your OTU table should be imported as a [QIIME 2 artifact](https://docs.qiime2.org/2018.2/concepts/#data-files-qiime-2-artifacts), with **OTUs in rows** and **samples in columns**.
Metadata should be a tab-delimited file with a column that contains samples labeled `case` and `control`.

If your OTU table is already a QIIME 2 artifact, you can skip directly to running the code.
Otherwise, follow the instructions below to use your own tab-delimited OTU table.

### Import tab-delimited OTU table into QIIME 2

You can use your own OTU table, or make a fake OTU table with `make_fake_data.py` in the `test_data/` folder here.

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

# To do's

* Update QIIME 2 downstream analyses to accept `FeatureTable[PercentileNormalized]`     
* Accept user-inputted case and control labels in column
* Make tutorial showing how to percentile normalize multiple datasets
    - download multiple feature tables; add case/control and study columns in the metadata
    - merge the feature tables (and metadata tables, if possible) with q2-feature-table
    - percentile normalize the data with the batch handling
* After PercentileNormalized is accepted into q2-types, remove declaration from here

# Versions

* 2018.10 - fix conflicting PercentileNormalize type after qiime2 2018.8 release
* 2018.4.2 - allow Numeric metadata column to specify batch    
* 2018.4.1 - add multiple batch handling in `percentile-normalize`     
* 2018.4.0 - initial plugin

## Compatibilities

q2-perc-norm versions 2018.4.* are not compatible with QIIME 2 versions
2018.8 or later. Similarly, q2-perc-norm version 2018.10 and later are not
compatible with QIIME 2 versions earlier than 2018.8.

# Updating conda build

This is the command to build an updated conda package:

```
conda-build pyinstrument/ \
 -c https://conda.anaconda.org/qiime2/label/r2018.8 \
 -c https://conda.anaconda.org/qiime2 \
 -c https://conda.anaconda.org/conda-forge \
 -c defaults \
 -c https://conda.anaconda.org/bioconda \
 -c https://conda.anaconda.org/biocore \
 --override-channels \
 --python 3.5
```
