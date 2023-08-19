# Test Documentation

## Plugin Name
q2-perc-norm
## Tester
Kingsley Apusiga (github.com/kingapus)

## Testing Environment(s)
1. QIIME2-2022.11
2. QIIME2-2023.7
   plugin was installed in the above conda environments for testing
   
## Installing modified plugin
1. Cloned the updated repository (branch repository)
2. uninstalled my the working version of the plugin that has the known issue ( ``` pip uninstall perc-norm```)
3. installed the modified plugin (cd into the new repository and run the command ```python setup.py install```

## Testing modified plugin
#### Input file: 
qiime FeatureTable[RelativeFrequency] artefact

#### Metadata: 
txt file with a column specifying which samples belong to the case or control group. [PRJEB50080 copy.txt](https://github.com/kingapus/q2-perc-norm/files/12386107/PRJEB50080.copy.txt)


#### test command
```
qiime perc-norm percentile-normalize \
--i-table table-no-mitoch-no-chloro-RF.qza \
--m-metadata-file ../PRJEB50080\ copy.txt \
--m-metadata-column status \
--o-perc-norm-table test_out.qza
```

#### test outcome
```
Saved FeatureTable[PercentileNormalized] to: test_out.qza
```
#### test issues
No issues were detected with this test
