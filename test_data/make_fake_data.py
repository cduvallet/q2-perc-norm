# Generate fake data
# 20 controls, 20 cases
# 10 OTUs with different sparsity in the controls

import pandas as pd
import numpy as np

n = 20
notus = 10

cols = ['otu' + str(i) for i in range(notus)]
inds = ['control' + str(i) for i in range(n)]\
    + ['case' + str(i) for i in range(n)]

df = pd.DataFrame(columns=cols, index=inds)
df.index.name = 'samples'
df.columns.name = 'otus'

for i in range(notus):
    h = np.random.uniform(size=int(n*i/10)).tolist() + [0]*int(n - n*i/10)
    c = np.random.uniform(size=int(n*i/10)).tolist() + [0]*int(n - n*i/10)

    df['otu' + str(i)] = h + c

df.to_csv('test_otu_table.txt', sep='\t')
df.T.to_csv('test_otu_table.transpose.txt', sep='\t')

# Make metadata for both applications
meta = pd.DataFrame(columns=['#SampleID', 'DiseaseState'])
meta['#SampleID'] = inds
meta['DiseaseState'] = ['control' for i in range(n)] \
    + ['case' for i in range(n)]

meta.to_csv('test_metadata.txt', sep='\t', index=False)

# And for Sean's version
with open('test_control_samples.txt', 'w') as f:
    f.write('\t'.join(inds[:n]))
with open('test_case_samples.txt', 'w') as f:
    f.write('\t'.join(inds[n:]))
