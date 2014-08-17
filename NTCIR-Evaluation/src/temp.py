#coding=utf8
from collections import defaultdict
import codecs
anno = defaultdict(lambda:0)
iddict =defaultdict(lambda:'')
queryweightsum = defaultdict(lambda:0)
for l in open('../data/temp/flsweight.txt'):
    segs = l.strip().split('\t')
    id = segs[0]
    fls = segs[1]
    weight = segs[5]
    anno[fls] = int(weight)
    iddict[fls] = id

for l in open('../data/temp/fls.txt'):
    id,fls = l.strip().split('\t')
    queryweightsum[iddict[fls]]+=anno[fls]
fout = open('../data/temp/flsposs.txt','w')
for l in open('../data/temp/fls.txt'):
    id,fls = l.strip().split('\t')
    print iddict[fls],fls,anno[fls],queryweightsum[iddict[fls]]
    fout.write(id+'\t'+fls+'\t'+str(float(anno[fls])/float(queryweightsum[iddict[fls]]))+'\n')
