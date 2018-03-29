# q2-perc-norm

QIIME2 plugin for percentile normalization to correct for batch effects in microbiome case-control studies

# Installing

First, make sure you've [installed qiime2](https://docs.qiime2.org/2018.2/install/) and are in the qiime2 virtual environment (`source activate qiime2-2018.2`)

Then, from the main folder run `python setup.py install`. Now, when you type `qiime` on the command line, the `perc-norm` plugin should show up in the list of available plugins.

# To do's

* Change output to be of class `FeatureTable[PercentileNormalized]`   
* Write actual documentation in this README   