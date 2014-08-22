__author__ = 'Administrator'

from collections import defaultdict
import os
import sys
dirname = 'enflseva'
tag = '0010'

run2id2dndcg = defaultdict(lambda:defaultdict(lambda: 'DEFAULT'))
run2id2dsharpndcg = defaultdict(lambda:defaultdict(lambda:  'DEFAULT'))
run2id2irecall = defaultdict(lambda:defaultdict(lambda:  'DEFAULT'))

for f in os.listdir('./'+dirname):
    run = f.split('.')[0]
    for l in open('./'+dirname+'/'+f):
        segs = filter(lambda x: len(x), l.strip().split(' '))
        if segs[1] == 'nDCG@'+tag+'=':
            num = float(segs[2])
            if num >1.0:
                num = 0.0
            run2id2dndcg[run][segs[0]]=str(num)
        if segs[1] == 'D#-nDCG@'+tag+'=':
            num = float(segs[2])
            if num >1.0:
                num = 0.0
            run2id2dsharpndcg[run][segs[0]]=str(num)
        if segs[1] == 'I-rec@'+tag+'=':
            num = float(segs[2])
            if num >1.0:
                num = 0.0
            run2id2irecall[run][segs[0]]=str(num)
fout = open(dirname+'.pertopic.csv','w')
fout.write('runname,id,nDCG@'+tag+',D#nDCG@'+tag+',I-rec@'+tag+'\n')

def union(s1,s2,s3):
    rtr  = set()
    for s in [s1,s2,s3]:
        for item in s:
            rtr.add(item)
    return rtr
for run in run2id2irecall.keys():
    for id in sorted(list(union(run2id2dndcg[run],run2id2dsharpndcg[run],run2id2irecall[run]))):
        print run,id
        fout.write(run+','+id+','+run2id2dndcg[run][id]+','+run2id2dsharpndcg[run][id]+','+run2id2irecall[run][id]+'\n')
fout.close()