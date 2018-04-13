# q2-perc-norm

QIIME 2 plugin for percentile normalization to correct for batch effects in microbiome case-control studies

# Installing

First, make sure you've [installed QIIME 2](https://docs.qiime2.org/2018.2/install/) and have activated the QIIME 2 virtual environment (`source activate qiime2-2018.2`).

Then, from the main folder run `python setup.py install`. Now, when you type `qiime` on the command line, the `perc-norm` plugin should show up in the list of available plugins.

# Using the plugin

Currently, the only method available in this plugin is `percentile-normalize`, which percentile normalizes the abundance of OTUs in case samples with respect to their abundance in control samples.

## Preparing your data

You'll need to prepare your OTU table and metadata file for use with this plugin.
Your OTU table should be imported as a [QIIME 2 artifact](https://docs.qiime2.org/2018.2/concepts/#data-files-qiime-2-artifacts), with OTUs in rows and samples in columns.
Metadata should be a tab-delimited file with a column that contains samples labeled `case` and `control`.

You can use your own OTU table, or make a fake OTU table with `make_fake_data.py` in the `test_data/` folder here.

If you're starting from a text file, you first need to convert the OTU table to biom format before you can import it into QIIME 2.

```
biom convert -i test_otu_table.transpose.txt -o test_otu_table.transpose.biom --table-type="OTU table" --to-hdf5
qiime tools import --input-path test_otu_table.transpose.biom --type 'FeatureTable[RelativeFrequency]' --source-format BIOMV210Format --output-path test_otu_table.transpose.qza
```

## Run percentile normalization

You then run the `percentile-normalize` script from the `perc-norm` qiime plugin.

```
qiime perc-norm percentile-normalize --i-table test_otu_table.transpose.qza --m-metadata-file test_metadata.txt --m-metadata-column DiseaseState --o-perc-norm-table test_out.percentile_qiime.qza
```

# To do's

* Make plugin conda-installable    
