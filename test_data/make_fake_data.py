# Generate fake data
# 20 controls, 20 cases
# 10 OTUs with different sparsity in the controls

import pandas as pd
import numpy as np

# n samples per batch
n = 20
# total OTUs
notus = 10
# number of batches
n_batches = 2

cols = ['otu' + str(i) for i in range(notus)]
inds = ['control' + str(i) for i in range(n)]\
    + ['case' + str(i) for i in range(n)]
inds = [i + '_' + str(b) for b in range(n_batches) for i in inds]

df = pd.DataFrame(columns=cols, index=inds)
df.index.name = 'samples'
df.columns.name = 'otus'

for b in range(n_batches):
    b_inds = [i for i in inds if i.endswith(str(b))]
    for i in range(notus):
        n_nonzero = n*(i+b) / float(n_batches + notus - 2)
        h = np.random.uniform(size=int(n_nonzero)).tolist() + [0]*int(n - n_nonzero)
        c = np.random.uniform(size=int(n_nonzero)).tolist() + [0]*int(n - n_nonzero)

        df.loc[b_inds, 'otu' + str(i)] = h + c

df.to_csv('test_otu_table.txt', sep='\t')
df.T.to_csv('test_otu_table.transpose.txt', sep='\t')

# Make metadata for both applications
meta = pd.DataFrame(columns=['#SampleID', 'DiseaseState'])
meta['#SampleID'] = inds
meta['DiseaseState'] = n_batches * (['control' for i in range(n)]
    + ['case' for i in range(n)])
batch_meta = []
for b in range(n_batches):
    batch_meta += ['batch' +  str(b)]*n*2
meta['batch'] = batch_meta

meta.to_csv('test_metadata.txt', sep='\t', index=False)

# And for Sean's version
with open('test_control_samples.txt', 'w') as f:
    f.write('\t'.join(inds[:n]))
with open('test_case_samples.txt', 'w') as f:
    f.write('\t'.join(inds[n:]))

# Make fake data to test the empty case/control labels

meta['disease_no_ctrl'] = meta['DiseaseState'].replace('control', 'contorl')
meta['disease_no_case'] = meta['DiseaseState'].replace('case', 'caes')
meta['disease_no_case_ctrl'] = meta['DiseaseState'].replace('control', 'contorl').replace('case', 'caes')
meta.to_csv('test_metadata.bad_case_ctrl_labels.txt', sep='\t', index=False)
