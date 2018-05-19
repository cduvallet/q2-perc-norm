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
