import numpy as np
import sys, os
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

# provide protein information
masterfile = open(sys.argv[1], 'r').readlines()
masterheader = masterfile[0].strip().split('\t')
masterinfo = []
for l, line in enumerate(masterfile):
        if l > 0:
            line = line.strip().split('\t')
            if ',' in line[masterheader.index('Motif_ID')]:
                rncmpt = line[masterheader.index('Motif_ID')].split(',')
            else:
                rncmpt = [line[masterheader.index('Motif_ID')]]
            for r, rnc in enumerate(rncmpt):
                nline = []
                for e, entry in enumerate(line):

                    if ',' in entry:
                        entry = entry.split(',')
                        if entry[0].isdigit():
                            entry = np.array(entry,dtype = int)
                    elif e == 8:
                        entry = [entry]
                    nline.append(entry)
                nline[1] = rnc
                for s in range(7):
                    nline[-s-1] = nline[-s-1][r]
                masterinfo.append(nline)
masterinfo = np.array(masterinfo)
doms = masterinfo[:,8]
motifs = masterinfo[:,1]

kmerfile = np.load(sys.argv[2])
kmerfeatures = kmerfile['features']
expnames = kmerfile['expnames']

groups = sys.argv[3].split(',')

groupkmer = []
for g, group in enumerate(groups):
    gset =[]
    for i, ina in enumerate(expnames):
        it = list(motifs).index(ina)
        domit = doms[it]
        if len(np.unique(domit)) == 1 and domit[0] == group:
            gset.append(np.where(kmerfeatures[:, i] != 0)[0])
    groupkmer.append(np.unique(np.concatenate(gset)))





if '--outdir' in sys.argv:
    outdir = sys.argv[sys.argv.index('--outdir')+1]
else:
    outdir = os.path.split(sys.argv[2])[0]
# First way to call the 2 group Venn diagram:
#venn2(subsets = (10, 5, 2), set_labels = ('Group A', 'Group B'))
#plt.show()
fig = plt.figure(figsize = (4,4))
ax = fig.add_subplot(111)
venn2([set(groupkmer[0]), set(groupkmer[1])], set_labels = groups, set_colors = ['royalblue', 'olive'], ax = ax)
fig.savefig(outdir+os.path.splitext(os.path.split(sys.argv[2])[1])[0]+'-'.join(np.array(groups))+'_vennkmer.jpg', bbox_inches = 'tight', dpi = 300)

if '--show' in sys.argv:
    plt.show()


